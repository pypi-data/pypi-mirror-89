#!/usr/bin/env python
# -*- coding: utf-8 -*-

# db.dicom_parser.py
"""Parse DICOM RT Dose, Structure, and Plan files for the DVH Analytics SQL Database"""
# Copyright (c) 2016-2019 Dan Cutright
# This file is part of DVH Analytics, released under a BSD license.
#    See the file LICENSE included with this distribution, also
#    available at https://github.com/cutright/DVH-Analytics

from dicompylercore import dvhcalc, dvh as dicompyler_dvh
from dicompylercore.dicomparser import DicomParser as dicompylerParser
from datetime import datetime
from dateutil.relativedelta import relativedelta  # python-dateutil
from dateutil.parser import parse as date_parser
import numpy as np
from os.path import basename, join
from pubsub import pub
import pydicom
from dvha.options import Options
from dvha.tools.errors import push_to_log
from dvha.tools.roi_name_manager import clean_name, DatabaseROIs
from dvha.tools.utilities import change_angle_origin, calc_stats, is_date, validate_transfer_syntax_uid
from dvha.tools.roi_formatter import dicompyler_roi_coord_to_db_string, get_planes_from_string
from dvha.tools import roi_geometry as roi_calc
from dvha.tools.mlc_analyzer import Beam as mlca
from dvha.db.sql_connector import DVH_SQL


class DICOM_Parser:
    """
    Parse a set of DICOM files for database
    """
    def __init__(self, plan_file=None, structure_file=None, dose_file=None, dose_sum_file=None, plan_over_rides=None,
                 global_plan_over_rides=None, roi_over_ride=None, roi_map=None, use_dicom_dvh=False, plan_ptvs=None, other_dicom_files=None):
        """
        :param plan_file: absolute path of DICOM RT Plan file
        :type plan_file: str
        :param structure_file: absolute path of DICOM RT Struct file
        :type structure_file: str
        :param dose_file: absolute path of DICOM RT Dose file
        :type dose_file: str
        :param dose_sum_file: DICOM RT Dose file with summed dose
        :type dose_sum_file: str
        :param plan_over_rides: Values from import GUI to override DICOM file data
        :type plan_over_rides: dict
        :param global_plan_over_rides: Values from import GUI to override DICOM file data
        :type global_plan_over_rides: dict
        :param roi_over_ride: lookup up for roi name and type overrides
        :type roi_over_ride: dict
        :param roi_map: roi name map
        :type roi_map: DatabaseROIs
        :param use_dicom_dvh: use the DVH stored in DICOM RT-Dose if it exists
        :type use_dicom_dvh: bool
        :param plan_ptvs: assign specifc PTVs for distance calculations
        :type plan_ptvs: list
        """

        self.database_rois = DatabaseROIs() if roi_map is None else roi_map

        options = Options()
        self.import_path = options.IMPORTED_DIR
        self.dvh_bin_max_dose = options.dvh_bin_max_dose
        self.dvh_bin_max_dose_units = options.dvh_bin_max_dose_units
        self.mlca_options = options.MLC_ANALYZER_OPTIONS
        self.get_dvh_kwargs = options.GET_DVH_KWARGS
        self.dvh_small_volume_threshold = options.DVH_SMALL_VOLUME_THRESHOLD
        self.dvh_high_resolution_factor = options.DVH_HIGH_RESOLUTION_FACTOR
        self.dvh_high_resolution_segments_between = options.DVH_HIGH_RESOLUTION_SEGMENTS_BETWEEN

        self.plan_file = plan_file
        self.structure_file = structure_file
        self.dose_file = dose_file
        self.dose_sum_file = dose_sum_file

        self.use_dicom_dvh = use_dicom_dvh

        # store these values when clearing file loaded data
        self.stored_values = {}

        self.rt_data = {key: None for key in ['plan', 'structure', 'dose']}
        self.dicompyler_data = {key: None for key in ['plan', 'structure', 'dose']}
        self.dicompyler_rt_plan = None
        self.structure_name_and_type = None
        if self.plan_file:
            self.dicompyler_data['plan'] = dicompylerParser(self.plan_file)
            self.rt_data['plan'] = self.dicompyler_data['plan'].ds
            self.dicompyler_rt_plan = self.dicompyler_data['plan'].GetPlan()
        if self.structure_file:
            self.dicompyler_data['structure'] = dicompylerParser(self.structure_file)
            self.rt_data['structure'] = self.dicompyler_data['structure'].ds
            self.structure_name_and_type = self.get_structure_name_and_type(self.rt_data['structure'])
        if self.dose_file:
            if self.dose_sum_file is None:
                # self.rt_data['dose'] = dicompylerParser(self.dose_file).ds
                # The above line may lead to OSError: Deferred read -- original filename not stored. Cannot re-open
                # switching back to pydicom.read_file()
                self.rt_data['dose'] = pydicom.read_file(self.dose_file, force=True)
            else:
                self.rt_data['dose'] = pydicom.read_file(self.dose_sum_file, force=True)

        # These properties are not inherently stored in Pinnacle DICOM files, but can be extracted from dummy ROI
        # names automatically generated by the Pinnacle Script provided by DVH Analytics
        self.poi_rx_data = self.get_rx_data_from_dummy_rois()
        self.poi_tx_site = self.get_tx_site_from_dummy_rois()

        self.__initialize_rx_beam_and_ref_beam_data()

        # over ride objects
        keys = ['mrn', 'study_instance_uid', 'birth_date', 'sim_study_date', 'physician', 'tx_site', 'rx_dose']
        self.plan_over_rides = [plan_over_rides, {key: None for key in keys}][plan_over_rides is None]
        self.global_plan_over_rides = global_plan_over_rides

        self.roi_over_ride = roi_over_ride if roi_over_ride is not None else {'name': {}, 'type': {}}
        for over_ride_type, over_ride in self.roi_over_ride.items():
            for key, value in over_ride.items():
                self.structure_name_and_type[key][over_ride_type] = value

        self.plan_ptvs = plan_ptvs
        self.other_dicom_files = other_dicom_files

    def update_stored_values(self):
        keys = ['study_instance_uid_to_be_imported', 'patient_name', 'mrn', 'sim_study_date', 'birth_date',
                'rx_dose', 'ptv_names', 'physician', 'ptv_exists', 'tx_site', 'patient_orientation']
        self.stored_values = {key: getattr(self, key) for key in keys}

    def __initialize_rx_beam_and_ref_beam_data(self):
        beam_num = 0
        self.rx_data = []
        self.beam_data = {}
        self.ref_beam_data = []
        for fx_grp_index, fx_grp_seq in enumerate(self.rt_data['plan'].FractionGroupSequence):
            self.rx_data.append(RxParser(self.rt_data['plan'], self.dicompyler_rt_plan, self.rt_data['structure'],
                                         fx_grp_index, self.poi_rx_data, self.study_instance_uid_to_be_imported))
            self.beam_data[fx_grp_index] = []
            for fx_grp_beam in range(int(fx_grp_seq.NumberOfBeams)):
                beam_number = self.beam_sequence[beam_num].BeamNumber
                beam_seq = self.beam_sequence[beam_num]
                cp_seq = self.get_cp_sequence(self.beam_sequence[beam_num])
                ref_beam_seq_index = self.get_referenced_beam_sequence_index(fx_grp_seq, beam_number)
                ref_beam_seq = fx_grp_seq.ReferencedBeamSequence[ref_beam_seq_index]
                self.beam_data[fx_grp_index].append(BeamParser(beam_seq, ref_beam_seq, cp_seq, self.mlca_options))

                beam_num += 1

    @staticmethod
    def get_referenced_beam_sequence_index(fx_grp_seq, beam_number):
        """
        Determine the index of the referenced beam sequence for a given beam_number. This properly connects BeamSequence
        beams and ReferencedBeamSequence beams.
        :param fx_grp_seq: Index of the fraction group (likely 0 unless TPS allows multiple prescriptions
        :param beam_number: The beam number of the beam of interest within BeamSequence
        :return: the ReferencedBeamSequence index that matches beam_number
        :rtype: int
        """
        for i, ref_beam_seq in enumerate(fx_grp_seq.ReferencedBeamSequence):
            if ref_beam_seq.ReferencedBeamNumber == beam_number:
                return i
        push_to_log(msg='DICOM_Parser: Failed to find a matching reference beam in '
                        'ReferencedBeamSequence for beam number %s' % beam_number)

    def get_rx_data_from_dummy_rois(self):
        """
        DVH Analytics allows for the user to indicate prescription information embedded in POI names. Some TPSs do not
        include prescription information in the exported DICOM Plan file. For example, Pinnacle scripts are provided
        by DVHA which will create these POIs.  The scripts are found in resources/Pinnacle Scripts

        A POI in the format:
            "rx#: <rx name>: <rx dose in cGy> cGy x <fxs> to <norm. %>%: <norm. method>: <norm. object>"
            where # is rx number starting from 1, will allow DVH-Analytics to retrieve rx information.
        :return: data for the Rxs table that can be extracted from POIs
        :rtype: dict
        """

        if self.structure_file:
            struct_seq = self.rt_data['structure'].StructureSetROISequence
            rx_indices = [i for i, roi in enumerate(struct_seq) if roi.ROIName.lower().startswith('rx ')]

            rx_data = {}
            for i in rx_indices:
                roi_name = struct_seq[i].ROIName.lower()
                name_split = roi_name.split(':')
                if len(name_split) > 3:
                    fx_grp_number = int(name_split[0].strip('rx '))
                    fx_grp_name = name_split[1].strip()
                    fx_dose = float(name_split[2].split('cgy')[0]) / 100.
                    fxs = int(name_split[2].split('x ')[1].split(' to')[0])
                    rx_dose = fx_dose * float(fxs)
                    rx_percent = float(name_split[2].strip().split(' ')[5].strip('%'))
                    normalization_method = name_split[3].strip()

                    if len(name_split) > 4:
                        normalization_object = ['plan_max', name_split[4].strip()][normalization_method != 'plan_max']
                    else:
                        normalization_object = None

                    rx_data[fx_grp_number] = {'fx_grp_number': fx_grp_number,
                                              'fx_grp_name': fx_grp_name,
                                              'fx_dose': fx_dose,
                                              'fxs': fxs,
                                              'rx_dose': rx_dose,
                                              'rx_percent': rx_percent,
                                              'normalization_method': normalization_method,
                                              'normalization_object': normalization_object}

            return rx_data

    def get_tx_site_from_dummy_rois(self):
        """
        DVH Analytics allows for the user to indicate treatment information embedded in POI names. By default, DVHA
        assumes the plan name is the tx site. However, if a POI is provided as follows, the tx site provided in the POI
        will be used instead. Pinnacle scripts are provided by DVHA which will create these POIs. The scripts are found
        in resources/Pinnacle Scripts
        A POI in the format:
            "tx: <site>"
            will allow DVH-Analytics to add this site name to the database upon import.
        :return: treatment site name
        :rtype: str
        """

        if self.structure_file:
            struct_seq = self.rt_data['structure'].StructureSetROISequence
            tx_indices = [i for i, roi in enumerate(struct_seq) if roi.ROIName.lower().startswith('tx: ')]

            if tx_indices:
                return struct_seq[tx_indices[0]].ROIName.split('tx: ')[1]

    def get_plan_row(self):
        """
        Get all data needed for a row in the Plans table of the database
        :return: plan row data with the column name as the key and the values are lists in the format
        [value, column variable type]. This object will be passed to DVH_SQL.insert_row
        :rtype: dict
        """

        return {'mrn': [self.mrn, 'text'],
                'study_instance_uid': [self.study_instance_uid_to_be_imported, 'text'],
                'birth_date': [self.birth_date, 'date'],
                'age': [self.age, 'smallint'],
                'patient_sex': [self.patient_sex, 'char(1)'],
                'sim_study_date': [self.sim_study_date, 'date'],
                'physician': [self.physician, 'varchar(50)'],
                'tx_site': [self.tx_site, 'varchar(50)'],
                'rx_dose': [self.rx_dose, 'real'],
                'fxs': [self.fxs_total, 'int'],
                'patient_orientation': [self.patient_orientation, 'varchar(3)'],
                'plan_time_stamp': [self.plan_time_stamp, 'timestamp'],
                'struct_time_stamp': [self.struct_time_stamp, 'timestamp'],
                'dose_time_stamp': [self.dose_time_stamp, 'timestamp'],
                'tps_manufacturer': [self.tps_manufacturer, 'varchar(50)'],
                'tps_software_name': [self.tps_software_name, 'varchar(50)'],
                'tps_software_version': [self.tps_software_version, 'varchar(30)'],
                'tx_modality': [self.tx_modality, 'varchar(30)'],
                'tx_time': [self.tx_time, 'time'],
                'total_mu': [self.total_mu, 'real'],
                'dose_grid_res': [self.dose_grid_res, 'varchar(16)'],
                'heterogeneity_correction': [self.heterogeneity_correction, ' varchar(30)'],
                'baseline': [None, 'boolean'],
                'import_time_stamp': [None, 'timestamp'],
                'protocol': [None, 'text'],
                'toxicity_grades': [None, 'text'],
                'complexity': [self.plan_complexity, 'real']}

    def get_beam_rows(self):
        """
        Get all beam rows across all prescriptions
        :return: a complete list of beam rows
        :rtype: list
        """
        beam_rows = []
        for rx_index, beam_set in self.beam_data.items():
            for beam in beam_set:
                if float(beam.beam_mu) > 0:  # Ignores set-up fields
                    beam_rows.append(self.get_beam_row(rx_index, beam))

        if len(beam_rows) == 0:
            return self.dummy_beam_row

        return beam_rows

    @property
    def dummy_beam_row(self):
        return [{'mrn': [self.mrn, 'text'],
                 'study_instance_uid': [self.study_instance_uid_to_be_imported, 'text'],
                 'import_time_stamp': [None, 'timestamp']}]

    def get_beam_row(self, rx_index, beam):
        """
        Get all data needed for a row in the Beams table of the database
        :param rx_index: the index of self.rx_data associated with beam
        :type rx_index: int
        :param beam: the beam data object to be parsed
        :type beam: BeamParser
        :return: beam row data with the column name as the key and the values are lists in the format
        [value, column variable type]. This object will be passed to DVH_SQL.insert_row
        :rtype: dict
        """
        rx = self.rx_data[rx_index]

        # store these getters so code is repeated every reference
        gantry_values = beam.gantry_values
        collimator_values = beam.collimator_values
        couch_values = beam.couch_values
        mlc_stat_data = beam.mlc_stat_data

        return {'mrn': [self.mrn, 'text'],
                'study_instance_uid': [self.study_instance_uid_to_be_imported, 'text'],
                'beam_number': [beam.beam_number, 'int'],
                'beam_name': [beam.beam_name, 'varchar(30)'],
                'fx_grp_number': [rx.fx_grp_number, 'smallint'],
                'fx_count': [rx.fx_count, 'int'],
                'fx_grp_beam_count': [rx.beam_count, 'smallint'],
                'beam_dose': [beam.beam_dose, 'real'],
                'beam_mu': [beam.beam_mu, 'real'],
                'radiation_type': [beam.radiation_type, 'varchar(30)'],
                'beam_energy_min': [beam.energy_min, 'real'],
                'beam_energy_max': [beam.energy_max, 'real'],
                'beam_type': [beam.beam_type, 'varchar(30)'],
                'control_point_count': [beam.control_point_count, 'int'],
                'gantry_start': [gantry_values['start'], 'real'],
                'gantry_end': [gantry_values['end'], 'real'],
                'gantry_rot_dir': [gantry_values['rot_dir'], 'varchar(5)'],
                'gantry_range': [gantry_values['range'], 'real'],
                'gantry_min': [gantry_values['min'], 'real'],
                'gantry_max': [gantry_values['max'], 'real'],
                'collimator_start': [collimator_values['start'], 'real'],
                'collimator_end': [collimator_values['end'], 'real'],
                'collimator_rot_dir': [collimator_values['rot_dir'], 'varchar(5)'],
                'collimator_range': [collimator_values['range'], 'real'],
                'collimator_min': [collimator_values['min'], 'real'],
                'collimator_max': [collimator_values['max'], 'real'],
                'couch_start': [couch_values['start'], 'real'],
                'couch_end': [couch_values['end'], 'real'],
                'couch_rot_dir': [couch_values['rot_dir'], 'varchar(5)'],
                'couch_range': [couch_values['range'], 'real'],
                'couch_min': [couch_values['min'], 'real'],
                'couch_max': [couch_values['max'], 'real'],
                'beam_dose_pt': [beam.beam_dose_pt, 'varchar(35)'],
                'isocenter': [beam.isocenter, 'varchar(35)'],
                'ssd': [beam.ssd, 'real'],
                'treatment_machine': [beam.treatment_machine, 'varchar(30)'],
                'scan_mode': [beam.scan_mode, 'varchar(30)'],
                'scan_spot_count': [beam.scan_spot_count, 'real'],
                'beam_mu_per_deg': [beam.beam_mu_per_deg, 'real'],
                'beam_mu_per_cp': [beam.beam_mu_per_cp, 'real'],
                'import_time_stamp': [None, 'timestamp'],
                'area_min': [mlc_stat_data['area'][5], 'real'],
                'area_mean': [mlc_stat_data['area'][3], 'real'],
                'area_median': [mlc_stat_data['area'][2], 'real'],
                'area_max': [mlc_stat_data['area'][0], 'real'],
                'perim_min': [mlc_stat_data['area'][5], 'real'],
                'perim_mean': [mlc_stat_data['area'][3], 'real'],
                'perim_median': [mlc_stat_data['area'][2], 'real'],
                'perim_max': [mlc_stat_data['area'][0], 'real'],
                'x_perim_min': [mlc_stat_data['x_perim'][5], 'real'],
                'x_perim_mean': [mlc_stat_data['x_perim'][3], 'real'],
                'x_perim_median': [mlc_stat_data['x_perim'][2], 'real'],
                'x_perim_max': [mlc_stat_data['x_perim'][0], 'real'],
                'y_perim_min': [mlc_stat_data['y_perim'][5], 'real'],
                'y_perim_mean': [mlc_stat_data['y_perim'][3], 'real'],
                'y_perim_median': [mlc_stat_data['y_perim'][2], 'real'],
                'y_perim_max': [mlc_stat_data['y_perim'][0], 'real'],
                'complexity_min': [mlc_stat_data['cmp_score'][5], 'real'],
                'complexity_mean': [mlc_stat_data['cmp_score'][3], 'real'],
                'complexity_median': [mlc_stat_data['cmp_score'][2], 'real'],
                'complexity_max': [mlc_stat_data['cmp_score'][0], 'real'],
                'cp_mu_min': [mlc_stat_data['cp_mu'][5], 'real'],
                'cp_mu_mean': [mlc_stat_data['cp_mu'][3], 'real'],
                'cp_mu_median': [mlc_stat_data['cp_mu'][2], 'real'],
                'cp_mu_max': [mlc_stat_data['cp_mu'][0], 'real'],
                'complexity': [mlc_stat_data['complexity'], 'real'],
                'tx_modality': [beam.tx_modality, 'varchar(35)']}

    def get_rx_rows(self):
        """
        Get all rx rows
        :return: a complete list of rx data objects
        :rtype: list
        """
        return [self.get_rx_row(rx) for rx in self.rx_data]

    def get_rx_row(self, rx):
        """
        Get all data needed for a row in the Rxs table of the database
        :param rx: a rx data object
        :type rx: RxParser
        :return: rx row data with the column name as the key and the values are lists in the format
        [value, column variable type]. This object will be passed to DVH_SQL.insert_row
        :rtype: dict
        """

        data = {'mrn': [self.mrn, 'text'],
                'study_instance_uid': [self.study_instance_uid_to_be_imported, 'text'],
                'plan_name': [rx.plan_name, 'varchar(50)'],
                'fx_grp_name': [rx.fx_grp_name, 'varchar(30)'],
                'fx_grp_number': [rx.fx_grp_number, 'smallint'],
                'fx_grp_count': [self.fx_grp_count, 'smallint'],
                'fx_dose': [rx.fx_dose, 'real'],
                'fxs': [rx.fx_count, 'smallint'],
                'rx_dose': [rx.rx_dose, 'real'],
                'rx_percent': [None, 'real'],
                'normalization_method': [rx.normalization_method, 'varchar(30)'],
                'normalization_object': [rx.normalization_object, 'varchar(30)'],
                'import_time_stamp': [None, 'timestamp']}

        # over-ride values if dummy roi's are used to store rx data in rt_structure
        if self.poi_rx_data and rx.fx_grp_number in list(self.poi_rx_data):
            for key, value in self.poi_rx_data[rx.fx_grp_number].items():
                data[key][0] = value

        for key, value in self.plan_over_rides.items():
            if key in data and value is not None:
                data[key][0] = value

        return data

    def get_dvh_row(self, dvh_index):
        """
        Get all data needed for a row in the DVHs table of the database
        :param dvh_index: the index of the ROI to be imported
        :type dvh_index: int
        :return: dvh row data with the column name as the key and the values are lists in the format
        [value, column variable type]. This object will be passed to DVH_SQL.insert_row
        :rtype: dict
        """

        # dicompyler-core expects integer limit in cGy
        # self.rx_dose in Gy, bin max is either in Gy or % Rx dose
        # This is needed to prevent np.histogram from blowing up memory usage
        # if no rx_dose is found, default to the absolute dose
        if self.rx_dose:
            limit = int(self.rx_dose * self.dvh_bin_max_dose[self.dvh_bin_max_dose_units])
        else:
            limit = int(self.dvh_bin_max_dose['Gy'] * 100.)

        dvh = None
        if self.use_dicom_dvh and self.dose_sum_file is None:
            try:
                dvh = dicompyler_dvh.DVH.from_dicom_dvh(self.rt_data['dose'], dvh_index)
            except AttributeError:  # dicompyler-core raises this if structure is not found in DICOM DVH
                pass

        if dvh is None:
            kwargs = {key: value for key, value in self.get_dvh_kwargs.items()}  # make copy
            kwargs['structure'] = self.rt_data['structure']
            kwargs['dose'] = self.rt_data['dose']
            kwargs['roi'] = dvh_index
            kwargs['limit'] = limit
            kwargs['callback'] = self.send_dvh_progress

            # Remove kwargs invalid before 0.5.6
            from dicompylercore import __version__ as dicompylercore_version
            if dicompylercore_version in ['0.5.4', '0.5.5']:
                if 'memmap_rtdose' in kwargs.keys():
                    kwargs.pop('memmap_rtdose')

            try:
                try:
                    dvh = dvhcalc.get_dvh(**kwargs)
                except AttributeError:
                    kwargs['dose'] = validate_transfer_syntax_uid(self.rt_data['dose'])
                    kwargs['structure'] = validate_transfer_syntax_uid(self.rt_data['structure'])
                    dvh = dvhcalc.get_dvh(**kwargs)
            except MemoryError:
                kwargs['memmap_rtdose'] = True
                dvh = dvhcalc.get_dvh(**kwargs)

            # If small volume, increase resolution
            if dvh.volume < self.dvh_small_volume_threshold:
                kwargs['interpolation_resolution'] = (self.rt_data['dose'].PixelSpacing[0] / self.dvh_high_resolution_factor,
                                                      self.rt_data['dose'].PixelSpacing[1] / self.dvh_high_resolution_factor)
                kwargs['interpolation_segments_between_planes'] = self.dvh_high_resolution_segments_between

                try:
                    dvh = dvhcalc.get_dvh(**kwargs)
                except MemoryError:
                    kwargs['memmap_rtdose'] = True
                    # dicompyler-core needs to re-parse the dose file
                    dvh = dvhcalc.get_dvh(**kwargs)

        if dvh and dvh.volume > 0:  # ignore points and empty ROIs
            geometries = self.get_dvh_geometries(dvh_index)

            return {'mrn': [self.mrn, 'text'],
                    'study_instance_uid': [self.study_instance_uid_to_be_imported, 'text'],
                    'institutional_roi': [self.get_institutional_roi(dvh_index), 'varchar(50)'],
                    'physician_roi': [self.get_physician_roi(dvh_index), 'varchar(50)'],
                    'roi_name': [self.get_roi_name(dvh_index), 'varchar(50)'],
                    'roi_type': [self.get_roi_type(dvh_index), 'varchar(20)'],
                    'volume': [dvh.volume, 'real'],
                    'min_dose': [dvh.min, 'real'],
                    'mean_dose': [dvh.mean, 'real'],
                    'max_dose': [dvh.max, 'real'],
                    'dvh_string': [','.join(['%.5f' % num for num in dvh.counts]), 'text'],
                    'roi_coord_string': [geometries['roi_coord_str'], 'text'],
                    'dist_to_ptv_min': [None, 'real'],
                    'dist_to_ptv_mean': [None, 'real'],
                    'dist_to_ptv_median': [None, 'real'],
                    'dist_to_ptv_max': [None, 'real'],
                    'surface_area': [geometries['surface_area'], 'real'],
                    'ptv_overlap': [None, 'real'],
                    'import_time_stamp': [None, 'timestamp'],
                    'centroid': [geometries['centroid'], 'varchar(35)'],
                    'dist_to_ptv_centroids': [None, 'real'],
                    'dth_string': [None, 'text'],
                    'spread_x': [geometries['spread'][0], 'real'],
                    'spread_y': [geometries['spread'][1], 'real'],
                    'spread_z': [geometries['spread'][2], 'real'],
                    'cross_section_max': [geometries['cross_sections']['max'], 'real'],
                    'cross_section_median': [geometries['cross_sections']['median'], 'real'],
                    'toxicity_grade': [None, 'smallint']}

    def get_dicom_file_row(self):
        """
        Get all data needed for a row in the DICOM_Files table of the database
        :return: dicom file data with the column name as the key and the values are lists in the format
        [value, column variable type]. This object will be passed to DVH_SQL.insert_row
        :rtype: dict
        """
        return {'mrn': [self.mrn, 'text'],
                'study_instance_uid': [self.study_instance_uid_to_be_imported, 'text'],
                'folder_path': [str(join(self.import_path, self.mrn)), 'text'],
                'plan_file': [basename(self.plan_file), 'text'],
                'structure_file': [basename(self.structure_file), 'text'],
                'dose_file': [basename(self.dose_file), 'text'],
                'import_time_stamp': [None, 'timestamp']}

    @property
    def mrn(self):
        if self.plan_over_rides['mrn'] is not None:
            return self.plan_over_rides['mrn']
        return self.rt_data['plan'].PatientID

    @property
    def study_instance_uid(self):
        return self.rt_data['plan'].StudyInstanceUID

    @property
    def study_instance_uid_to_be_imported(self):
        if hasattr(self, 'plan_over_rides') and self.plan_over_rides['study_instance_uid']:
            return self.plan_over_rides['study_instance_uid']
        return self.rt_data['plan'].StudyInstanceUID

    @property
    def is_study_instance_uid_valid(self):
        return self.is_uid_valid(self.study_instance_uid)

    @property
    def is_study_instance_uid_to_be_imported_valid(self):
        return self.is_uid_valid(self.study_instance_uid_to_be_imported)

    @staticmethod
    def is_uid_valid(uid):
        valid = False
        if uid:
            with DVH_SQL() as cnx:
                valid = not cnx.is_study_instance_uid_in_table('Plans', uid)
        return valid

    @property
    def patient_name(self):
        return str(self.rt_data['plan'].PatientName)

    @property
    def file_set_complete(self):
        return all([self.plan_file, self.structure_file, self.dose_file])

    @property
    def missing_files(self):
        return [key.capitalize() for key, value in self.rt_data.items() if value is None]

    # ------------------------------------------------------------------------------
    # Plan table data
    # ------------------------------------------------------------------------------
    @property
    def tx_modality(self):
        tx_modalities = []
        for fx_grp_index, beam_parser_list in self.beam_data.items():
            for beam_parser in beam_parser_list:
                tx_modalities.append(beam_parser.tx_modality)
        tx_modalities = sorted(list(set(tx_modalities)))
        return ','.join(tx_modalities)

    @property
    def rx_dose(self):
        if self.plan_over_rides['rx_dose'] is not None:
            ans = self.plan_over_rides['rx_dose']
        elif self.poi_rx_data:
            ans = sum([rx['rx_dose'] for rx in self.poi_rx_data.values()])
        else:
            ans = sum([rx.rx_dose for rx in self.rx_data if rx.rx_dose])
        return self.process_global_over_ride('rx_dose', ans)

    @property
    def total_mu(self):
        mus = []
        for fx_grp_index, beam_parser_list in self.beam_data.items():
            for beam_parser in beam_parser_list:
                if self.rx_data[fx_grp_index].fx_count:
                    if beam_parser.beam_mu:
                        mus.append(beam_parser.beam_mu * self.rx_data[fx_grp_index].fx_count)
        return sum(mus)

    @property
    def heterogeneity_correction(self):
        if hasattr(self.rt_data['dose'], 'TissueHeterogeneityCorrection'):
            if isinstance(self.rt_data['dose'].TissueHeterogeneityCorrection, str):
                heterogeneity_correction = self.rt_data['dose'].TissueHeterogeneityCorrection
            else:
                heterogeneity_correction = ','.join(self.rt_data['dose'].TissueHeterogeneityCorrection)
        else:
            heterogeneity_correction = 'IMAGE'

        return heterogeneity_correction

    @property
    def patient_sex(self):
        return self.get_attribute('plan', 'PatientSex')

    @property
    def sim_study_date(self):
        if self.plan_over_rides['sim_study_date'] is not None:
            ans = self.plan_over_rides['sim_study_date']
        else:
            ans = self.get_attribute('plan', 'StudyDate')
            if not ans:
                ans = self.find_first_value_from_other_dicom_files('StudyDate')
                ans = ans if ans else ''
        ans = self.process_global_over_ride('sim_study_date', ans)
        return self.process_global_over_ride('sim_study_date', ans)

    @property
    def birth_date(self):
        if self.plan_over_rides['birth_date'] is not None:
            ans = self.plan_over_rides['birth_date']
        else:
            ans = self.get_attribute('plan', 'PatientBirthDate')
        return self.process_global_over_ride('birth_date', ans)

    @property
    def age(self):
        if self.sim_study_date and self.birth_date:
            try:
                dates = {'sim_study_date': None, 'birth_date': None}
                for date_type in list(dates):
                    dates[date_type] = getattr(self, date_type)
                    if type(dates[date_type]) is int or float:
                        dates[date_type] = str(dates[date_type])
                    if type(dates[date_type]) is str:
                        dates[date_type] = date_parser(dates[date_type]).date()
                age = relativedelta(dates['sim_study_date'], dates['birth_date']).years
                if age >= 0:
                    return age
            except Exception:
                pass

    @property
    def physician(self):
        if self.plan_over_rides['physician'] is not None:
            ans = self.plan_over_rides['physician']
        else:
            ans = str(self.get_attribute('plan', ['PhysiciansOfRecord', 'ReferringPhysicianName'])).upper()
            if not ans:
                ans = 'DEFAULT'
        return self.process_global_over_ride('physician', ans)

    @property
    def fxs(self):
        try:
            fx_grp_seq = self.rt_data['plan'].FractionGroupSequence
            return [int(float(fx_grp.NumberOfFractionsPlanned)) for fx_grp in fx_grp_seq]
        except ValueError:
            pass

    @property
    def fxs_total(self):
        fxs = self.fxs
        if fxs:
            return sum(fxs)

    @property
    def fx_grp_count(self):
        return len(self.rt_data['plan'].FractionGroupSequence)

    @property
    def patient_orientation(self):
        # TODO: database assumes only one orientation (i.e., three characters)
        seq = self.get_attribute('plan', 'PatientSetupSequence')
        if seq is not None:
            # return ','.join([setup.PatientPosition for setup in seq])
            ans = str(seq[0].PatientPosition)
            return ans if len(ans) < 4 else ans[:3]

    @property
    def plan_time_stamp(self):
        return self.get_time_stamp('plan')

    @property
    def struct_time_stamp(self):
        return self.get_time_stamp('structure')

    @property
    def dose_time_stamp(self):
        return self.get_time_stamp('dose')

    @property
    def tps_manufacturer(self):
        return self.get_attribute('plan', 'Manufacturer')

    @property
    def tps_software_name(self):
        return self.get_attribute('plan', 'ManufacturerModelName')

    @property
    def tps_software_version(self):
        # Some TPSs may store the version in RT Dose rather than plan
        # SoftwareVersions may also be stored as a string rather than a list
        for rt_type in ['plan', 'dose', 'structure']:  # Check each rt_type until SoftwareVersions is found
            version = self.get_attribute(rt_type, 'SoftwareVersions')
            if version is not None:
                if isinstance(version, str):
                    version = [version]
                return ','.join(version)

    @property
    def tx_site(self):
        if self.plan_over_rides['tx_site'] is not None:
            ans = self.plan_over_rides['tx_site']
        elif self.poi_tx_site is not None:
            ans = self.poi_tx_site
        else:
            ans = self.get_attribute('plan', 'RTPlanLabel')
        return self.process_global_over_ride('tx_site', ans)

    @property
    def brachy(self):
        return hasattr(self.rt_data['plan'], 'BrachyTreatmentType')

    @property
    def brachy_type(self):
        return self.get_attribute('plan', 'BrachyTreatmentType')

    @property
    def proton(self):
        return hasattr(self.rt_data['plan'], 'IonBeamSequence')

    @property
    def beam_sequence(self):
        if hasattr(self.rt_data['plan'], 'BeamSequence'):
            return self.rt_data['plan'].BeamSequence
        elif hasattr(self.rt_data['plan'], 'IonBeamSequence'):
            return self.rt_data['plan'].IonBeamSequence

    def get_cp_sequence(self, beam_seq):
        if hasattr(beam_seq, 'ControlPointSequence'):
            return beam_seq.ControlPointSequence
        elif hasattr(beam_seq, 'IonControlPointSequence'):
            return beam_seq.IonControlPointSequence

    @property
    def photon(self):
        return self.is_beam_with_rad_type_in_plan('photon')

    @property
    def electron(self):
        return self.is_beam_with_rad_type_in_plan('electron')

    @property
    def radiation_type(self):
        rad_types = {'PHOTONS': self.photon,
                     'ELECTRONS': self.electron,
                     'PROTONS': self.proton,
                     'BRACHY': self.brachy_type}
        types = sorted([rad_type for rad_type, rad_value in rad_types.items() if rad_value])
        return ','.join(types)

    @property
    def tx_time(self):
        if hasattr(self.rt_data['plan'], 'BrachyTreatmentType') and \
                hasattr(self.rt_data['plan'], 'ApplicationSetupSequence'):
            seconds = 0
            for app_seq in self.rt_data['plan'].ApplicationSetupSequence:
                for chan_seq in app_seq.ChannelSequence:
                    seconds += chan_seq.ChannelTotalTime
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            return "%02d:%02d:%02d" % (h, m, s)

    @property
    def dose_grid_res(self):
        try:
            dose_grid_resolution = [str(round(float(self.rt_data['dose'].PixelSpacing[0]), 1)),
                                    str(round(float(self.rt_data['dose'].PixelSpacing[1]), 1))]
            if hasattr(self.rt_data['dose'], 'SliceThickness') and self.rt_data['dose'].SliceThickness:
                dose_grid_resolution.append(str(round(float(self.rt_data['dose'].SliceThickness), 1)))
            return ', '.join(dose_grid_resolution)
        except Exception:
            pass

    def process_global_over_ride(self, key, pre_over_ride_value):
        if self.global_plan_over_rides:
            over_ride = self.global_plan_over_rides[key]
            if over_ride['value']:
                if not over_ride['only_if_missing'] or (over_ride['only_if_missing'] and not pre_over_ride_value):
                    return over_ride['value']
        return pre_over_ride_value

    @property
    def plan_complexity(self):
        plan_complexity = 0
        fx_counts = self.fxs
        for fx_index, fx in self.beam_data.items():
            fxs = fx_counts[fx_index]
            for beam in fx:
                complexity = beam.mlc_stat_data['complexity']
                if complexity:
                    plan_complexity += complexity * fxs
        if plan_complexity:
            return plan_complexity / sum(fx_counts)

    # ------------------------------------------------------------------------------
    # DVH table data
    # ------------------------------------------------------------------------------
    def get_roi_type(self, key):
        """
        Get the ROI type as defined in DICOM (e.g., PTV, ORGAN, EXTERNAL, etc.)
        :param key: index of ROI
        :type key: int
        :return: the roi type
        :rtype: str
        """
        if key in list(self.roi_over_ride['type']):
            return self.roi_over_ride['type'][key]

        roi_type_from_roi_map = self.database_rois.get_roi_type(self.physician, self.get_physician_roi(key))
        if roi_type_from_roi_map != 'NONE':
            return roi_type_from_roi_map

        return str(self.structure_name_and_type[key]['type']).upper()

    def reset_roi_type_over_ride(self, key):
        self.roi_over_ride['type'][key] = None

    def get_roi_name(self, key):
        """
        :param key: the index of the roi
        :return: roi name to be used in the database
        :rtype: str
        """
        if key in list(self.roi_over_ride['name']):
            return clean_name(self.roi_over_ride['name'][key])
        return clean_name(self.structure_name_and_type[key]['name'])

    def get_physician_roi(self, key):
        """
        Look up the physician roi of the specified roi for this plan
        :param key: the index of the roi
        :return: physician roi or 'uncategorized'
        :rtype: str
        """
        roi_name = self.get_roi_name(key)
        if self.database_rois.is_roi(roi_name):
            if self.database_rois.is_physician(self.physician):
                return self.database_rois.get_physician_roi(self.physician, roi_name)
        return 'uncategorized'

    def get_institutional_roi(self, key):
        """
        Look up the institutional roi of the specified roi for this plan
        :param key: the index of the roi
        :return: institutional roi or 'uncategorized'
        :rtype: str
        """
        roi_name = self.get_roi_name(key)
        if self.database_rois.is_roi(roi_name):
            if self.database_rois.is_physician(self.physician):
                return self.database_rois.get_institutional_roi(self.physician, self.get_physician_roi(key))
            if roi_name in self.database_rois.institutional_rois:
                return roi_name
        return 'uncategorized'

    @property
    def ptv_exists(self):
        """
        Check if the plan has at least one PTV assigned
        :rtype: bool
        """
        if self.structure_name_and_type:
            for key in list(self.structure_name_and_type):
                if self.get_roi_type(key) == 'PTV':
                    return True
        return False

    @property
    def roi_names(self):
        """
        :return: roi_names for this plan per the plan (clean_name not applied)
        :rtype: list
        """
        return [self.get_roi_name(key) for key in list(self.structure_name_and_type)]

    def get_roi_key(self, roi_name):
        """
        Look-up the roi index for a given roi_name
        :param roi_name: the ROI name to be looked-up
        :return: the roi index or None
        :rtype: int
        """
        roi_name = clean_name(roi_name)
        for key in list(self.structure_name_and_type):
            if roi_name == clean_name(self.get_roi_name(key)):
                return key

    @property
    def ptv_names(self):
        """
        Scan all ROIs for PTVs
        :return: PTV names
        :rtype: list
        """
        if self.structure_name_and_type:
            return [self.get_roi_name(x) for x in list(self.structure_name_and_type) if self.get_roi_type(x) == 'PTV']
        return self.stored_values['ptv_names']

    def get_surface_area(self, key):
        """
        :param key: the index of the roi
        :return: the surface area of the ROI in cm^2
        :rtype: float
        """
        coord = self.dicompyler_data['structure'].GetStructureCoordinates(key)
        try:
            return roi_calc.surface_area(coord)
        except Exception as e:
            msg = "DICOM_Parser: Surface area calculation failed for key, name: %s, %s" % (key, self.get_roi_name(key))
            push_to_log(e, msg=msg)

    def get_dvh_geometries(self, key):
        """
        Collect ROI geometry information to be stored in the database
        :param key: the index of the roi
        :return: geometric information
        :rtype: dict
        """

        structure_coord = self.dicompyler_data['structure'].GetStructureCoordinates(key)

        try:
            surface_area = roi_calc.surface_area(structure_coord)
        except Exception as e:
            msg = "DICOM_Parser: Surface area calculation failed for key, name: %s, %s" % (key, self.get_roi_name(key))
            push_to_log(e, msg=msg)
            surface_area = None

        roi_coord_str = dicompyler_roi_coord_to_db_string(structure_coord)
        planes = get_planes_from_string(roi_coord_str)
        centroid = roi_calc.centroid(planes)
        spread = roi_calc.spread(planes)
        cross_sections = roi_calc.cross_section(planes)

        return {'roi_coord_str': roi_coord_str,
                'surface_area': surface_area,
                'centroid': ','.join([str(round(x, 3)) for x in centroid]),
                'spread': spread,
                'cross_sections': cross_sections}

    # ------------------------------------------------------------------------------
    # Generic tools
    # ------------------------------------------------------------------------------
    @property
    def init_param(self):
        params = ['plan_file', 'structure_file', 'dose_file', 'dose_sum_file',
                  'plan_over_rides', 'global_plan_over_rides', 'roi_over_ride']
        return {key: getattr(self, key) for key in params}

    def get_attribute(self, rt_type, pydicom_attribute):
        """
        :param rt_type: plan. dose, or structure
        :type rt_type: str
        :param pydicom_attribute: attribute as specified in pydicom
        :type pydicom_attribute: str or list of str
        :return: pydicom value or None
        """
        if isinstance(pydicom_attribute, str):
            pydicom_attribute = [pydicom_attribute]

        for attribute in pydicom_attribute:
            if hasattr(self.rt_data[rt_type], attribute):
                return getattr(self.rt_data[rt_type], attribute)

    def get_time_stamp(self, rt_type):
        """
        Get the time stamp as specified in the DICOM file
        :param rt_type: 'plan', 'structure' or 'dose'
        :return: datetime
        :type: datetime
        """

        attribute = {'date': {'plan': 'RTPlanDate',
                              'structure': 'StructureSetDate',
                              'dose': 'InstanceCreationDate'},
                     'time': {'plan': 'RTPlanTime',
                              'structure': 'StructureSetTime',
                              'dose': 'InstanceCreationTime'}}

        datetime_str = self.get_attribute(rt_type, attribute['date'][rt_type])
        time = self.get_attribute(rt_type, attribute['time'][rt_type])

        try:
            if time:
                time = time.split('.')[0]  # ignore fractional sec
                return datetime.strptime(datetime_str + time, '%Y%m%d%H%M%S')
            else:
                return datetime.strptime(datetime_str, '%Y%m%d')
        except Exception as e:
            push_to_log(e, msg="DICOM_Parser: get_time_stamp failed")

    def is_beam_with_rad_type_in_plan(self, rad_type):
        """
        If a beam is photon or electron, beam data is stored in BeamSequence as opposed to IonBeamSequence
        :param rad_type: the radiation type of the beam (e.g., 'photon' or 'electron')
        :type rad_type: str
        :return: True if any beam in plan is the specified rad_type
        :rtype: bool
        """
        if hasattr(self.rt_data['plan'], 'BeamSequence'):
            for beam in self.rt_data['plan'].BeamSequence:
                if rad_type in beam.RadiationType:
                    return True
        return False

    @property
    def pre_import_data(self):
        """
        :return: Only the data needed for the pre import screen, pass to PreImportData
        :rtype: dict
        """
        self.update_stored_values()
        return {'file_set': {'plan': self.plan_file, 'dose': self.dose_file, 'structure': self.structure_file},
                'stored_values': self.stored_values,
                'dicompyler_rt_structures': self.structure_name_and_type,
                'roi_map': self.database_rois}

    @staticmethod
    def get_structure_name_and_type(rt_struct_ds):
        """Stripped down version of dicompylercore.dicomparser.GetStructures"""
        structures = {}

        # Locate the name and number of each ROI
        if 'StructureSetROISequence' in rt_struct_ds:
            for item in rt_struct_ds.StructureSetROISequence:
                data = {}
                number = int(item.ROINumber)
                data['id'] = number
                data['name'] = item.ROIName
                structures[number] = data

        # Determine the type of each structure (PTV, organ, external, etc)
        if 'RTROIObservationsSequence' in rt_struct_ds:
            for item in rt_struct_ds.RTROIObservationsSequence:
                number = item.ReferencedROINumber
                if number in structures:
                    structures[number]['type'] = item.RTROIInterpretedType

        return structures

    @staticmethod
    def send_dvh_progress(current_plane, plane_count):
        """
        Callback for dicompyler-core dvh calculation
        :param current_plane: the plane to be calculated
        :type current_plane: int
        :param plane_count: total number of planes to be calculated
        :type plane_count: int
        """
        progress = float(current_plane) / float(plane_count)
        pub.sendMessage('update_dvh_progress', msg=progress)

    def find_first_value_from_other_dicom_files(self, attr):
        if self.other_dicom_files and self.study_instance_uid in self.other_dicom_files:
            for f in self.other_dicom_files[self.study_instance_uid]:
                ds = pydicom.read_file(f)
                modality = getattr(ds, 'Modality')
                if modality.lower() in ['ct', 'mr'] and hasattr(ds, attr):
                    return getattr(ds, attr)


class BeamParser:
    """
    This class is used to parse beam data needed for importing a plan into the database
    """
    def __init__(self, beam_data, ref_beam_data, cp_seq, mlc_analyzer_options):
        """
        :param beam_data:
        :param ref_beam_data:
        :param cp_seq:
        """
        self.beam_data = beam_data
        self.ref_beam_data = ref_beam_data
        self.cp_seq = cp_seq
        self.options = mlc_analyzer_options

    ################################################################################
    # General beam parser tools
    ################################################################################
    @staticmethod
    def get_data_attribute(data_obj, pydicom_attr, default=None, data_type=None):
        """
        Generic method to get the value of a pydicom dataset attribute
        :param data_obj: a pydicom dataset
        :param pydicom_attr: the attribute of interest
        :type pydicom_attr: str
        :param default: if attribute is not found, this value is returned
        :param data_type: set to 'float' or 'int' to convert return value as specified
        :type data_type: str
        :return: the value of the pydicom attribute
        """
        if hasattr(data_obj, pydicom_attr):
            value = getattr(data_obj, pydicom_attr)
            if data_type == 'float':
                return float(value)
            elif data_type == 'int':
                return int(float(value))
            return value
        return default

    def get_point_attribute(self, data_obj, pydicom_attr):
        """
        Generic method to get the value of a pydicom dataset attribute that represents a point
        :param data_obj: a pydicom dataset
        :param pydicom_attr: the attribute of interest
        :return: a csv of the point values
        :rtype: str
        """
        point = self.get_data_attribute(data_obj, pydicom_attr)
        if point:
            return ','.join([str(round(dim_value, 3)) for dim_value in point])

    def get_cp_attributes(self, pydicom_attr, force_float=False, force_int=False):
        """
        Generic method to get the values of a pydicom attribute for self.cp_seqeunce
        This is used anytime you need to retrieve values that are specified for every control point
        :param pydicom_attr: the attribute of interest
        :type pydicom_attr: str
        :param force_float: force values to be of type float
        :type force_float: bool
        :param force_int: force values to eb of type int
        :type force_int: bool
        :return: the values of the specified attribute across all control points
        :rtype: list
        """
        values = []
        for cp in self.cp_seq:
            if hasattr(cp, pydicom_attr):
                if 'Rotation' in pydicom_attr:
                    if getattr(cp, pydicom_attr).upper() in {'CC', 'CW'}:
                        values.append(getattr(cp, pydicom_attr).upper())
                else:
                    value = getattr(cp, pydicom_attr)
                    if force_float:
                        value = float(value)
                    if force_int:
                        value = int(float(value))
                    values.append(value)

        if pydicom_attr[-5:] == 'Angle':
            values = change_angle_origin(values, 180)  # if angle is greater than 180, convert to negative value
        return values

    def get_angle_values(self, angle_type):
        """
        Collect data to be used for database import related to objects that have angles
        :param angle_type: 'gantry', 'collimator' or 'couch'
        :type angle_type: 'str
        :return: start, end, rot_dir, range, min, and max values
        :rtype: dict
        """
        angles = getattr(self, '%s_angles' % angle_type)
        return {'start': angles[0],
                'end': angles[-1],
                'rot_dir': self.get_rotation_direction(getattr(self, '%s_rot_dirs' % angle_type)),
                'range': round(float(np.sum(np.abs(np.diff(angles)))), 1),
                'min': min(angles),
                'max': max(angles)}

    @staticmethod
    def get_rotation_direction(rotation_list):
        """
        Given a list of rotation directions, return either the only direction or both with the initial direction first
        :param rotation_list: rotation angles of a beam attribute
        :return: concise description of rotation
        :rtype: str
        """
        if not rotation_list:
            return None
        if len(set(rotation_list)) == 1:  # Only one direction found
            return rotation_list[0]
        return ['CC/CW', 'CW/CC'][rotation_list[0] == 'CW']

    ################################################################################
    # Properties
    ################################################################################
    @property
    def beam_number(self):
        return int(self.beam_data.BeamNumber)

    @property
    def beam_name(self):
        if hasattr(self.beam_data, 'BeamDescription'):
            return self.beam_data.BeamDescription
        if hasattr(self.beam_data, 'BeamName'):
            return self.beam_data.BeamName
        return self.beam_number

    @property
    def treatment_machine(self):
        return self.get_data_attribute(self.beam_data, 'TreatmentMachineName')

    @property
    def beam_dose(self):
        return self.get_data_attribute(self.ref_beam_data, 'BeamDose', default=0., data_type='float')

    @property
    def beam_mu(self):
        return self.get_data_attribute(self.ref_beam_data, 'BeamMeterset', default=0., data_type='float')

    @property
    def beam_dose_pt(self):
        return self.get_point_attribute(self.ref_beam_data, 'BeamDoseSpecificationPoint')

    @property
    def isocenter(self):
        return self.get_point_attribute(self.cp_seq[0], 'IsocenterPosition')

    @property
    def beam_type(self):
        return self.get_data_attribute(self.beam_data, 'BeamType')

    @property
    def radiation_type(self):
        return self.get_data_attribute(self.beam_data, 'RadiationType')

    @property
    def scan_mode(self):
        return self.get_data_attribute(self.beam_data, 'ScanMode')

    @property
    def scan_spot_count(self):
        if hasattr(self.cp_seq[0], 'NumberOfScanSpotPositions'):
            return sum([int(cp.NumberOfScanSpotPositions) for cp in self.cp_seq]) / 2

    @property
    def energies(self):
        return self.get_cp_attributes('NominalBeamEnergy')

    @property
    def energy_min(self):
        return round(min(self.energies), 2)

    @property
    def energy_max(self):
        return round(max(self.energies), 2)

    @property
    def gantry_angles(self):
        return self.get_cp_attributes('GantryAngle', force_float=True)

    @property
    def collimator_angles(self):
        return self.get_cp_attributes('BeamLimitingDeviceAngle', force_float=True)

    @property
    def couch_angles(self):
        return self.get_cp_attributes('PatientSupportAngle', force_float=True)

    @property
    def gantry_rot_dirs(self):
        return self.get_cp_attributes('GantryRotationDirection', force_float=True)

    @property
    def collimator_rot_dirs(self):
        return self.get_cp_attributes('BeamLimitingDeviceRotationDirection')

    @property
    def couch_rot_dirs(self):
        return self.get_cp_attributes('PatientSupportRotationDirection')

    @property
    def gantry_values(self):
        return self.get_angle_values('gantry')

    @property
    def collimator_values(self):
        return self.get_angle_values('collimator')

    @property
    def couch_values(self):
        return self.get_angle_values('couch')

    @property
    def is_arc(self):
        return bool(self.get_angle_values('gantry')['rot_dir'])

    @property
    def tx_modality(self):
        rad_type = str(self.radiation_type)
        if not rad_type:
            return None
        if 'brachy' in rad_type.lower():
            return rad_type
        return "%s %s" % (self.radiation_type.title(), ['3D', 'Arc'][self.is_arc])

    @property
    def control_point_count(self):
        return int(self.get_data_attribute(self.beam_data, 'NumberOfControlPoints'))

    @property
    def ssd(self):
        ssds = self.get_cp_attributes('SourceToSurfaceDistance', force_float=True)
        if ssds:
            return round(float(np.average(ssds))/10., 2)

    @property
    def beam_mu_per_deg(self):
        try:
            return round(self.beam_mu / self.gantry_values['range'], 2)
        except Exception:
            pass

    @property
    def beam_mu_per_cp(self):
        try:
            return round(self.beam_mu / self.control_point_count, 2)
        except Exception:
            pass

    @property
    def mlc_stat_data(self):
        mlc_keys = ['area', 'x_perim', 'y_perim', 'perim', 'cmp_score', 'cp_mu']
        try:
            mlc_summary_data = mlca(self.beam_data, self.beam_mu, ignore_zero_mu_cp=True, **self.options).summary
            mlca_stat_data = {key: calc_stats(mlc_summary_data[key]) for key in mlc_keys}
            mlca_stat_data['complexity'] = np.sum(mlc_summary_data['cmp_score'])
        except Exception as e:
            push_to_log(e, msg='BeamParser: skipping mlc_stat_data calculation')
            mlca_stat_data = {key: [None] * 6 for key in mlc_keys}
            mlca_stat_data['complexity'] = None
        return mlca_stat_data


class RxParser:
    """
    This class is used to parse rx data needed for importing a plan into the database
    """
    def __init__(self, rt_plan, dicompyler_plan, rt_structure, fx_grp_index, pinnacle_rx_data, study_instance_uid):
        """
        :param rt_plan: the pydicom dataset object from reading the RT Plan DICOM file
        :param dicompyler_plan: the dicompyler-core object from readying the RT Plan DICOM file
        :param rt_structure: the pydicom dataset object from reading the RT Structure DICOM file
        :param fx_grp_index: the index of the fraction group associated with the rx to be parsed
        :type fx_grp_index: int
        :param pinnacle_rx_data: prescription data extracted from dummy POIs
        :type pinnacle_rx_data: dict
        :param study_instance_uid: The study instance UID of the associated plan.
        :type study_instance_uid: str
        """
        self.rt_plan = rt_plan
        self.dicompyler_plan = dicompyler_plan
        self.rt_structure = rt_structure
        self.study_instance_uid = study_instance_uid
        self.fx_grp_data = rt_plan.FractionGroupSequence[fx_grp_index]
        self.dose_ref_index = self.get_dose_ref_seq_index()

        self.pinnacle_rx_data = None
        if pinnacle_rx_data and fx_grp_index+1 in list(pinnacle_rx_data):
            self.pinnacle_rx_data = pinnacle_rx_data[fx_grp_index+1]

    ################################################################################
    # General rx parser tools
    ################################################################################
    def get_dose_ref_seq_index(self):
        if self.has_dose_ref:
            for i, dose_ref in enumerate(self.rt_plan.DoseReferenceSequence):
                if dose_ref.DoseReferenceNumber == self.fx_grp_number:
                    return i

    def get_dose_ref_attr(self, pydicom_attr):
        if self.has_dose_ref and self.dose_ref_index is not None:
            dose_ref_data = self.rt_plan.DoseReferenceSequence[self.dose_ref_index]
            if hasattr(dose_ref_data, pydicom_attr):
                return getattr(dose_ref_data, pydicom_attr)

    ################################################################################
    # Properties
    ################################################################################
    @property
    def plan_name(self):
        if hasattr(self.rt_plan, 'RTPlanLabel'):
            return self.rt_plan.RTPlanLabel

    @property
    def fx_grp_number(self):
        """
        If there are multiple RT Plan files for a given study instance uid, this function will ensure fx_grp_number
        is unique
        :rtype: int
        """
        with DVH_SQL() as cnx:
            fraction_group_start = cnx.get_max_value('Rxs', 'fx_grp_number',
                                                     "study_instance_uid = '%s'" % self.study_instance_uid)
        if not fraction_group_start:
            fraction_group_start = 0
        return self.fx_grp_data.FractionGroupNumber + fraction_group_start

    @property
    def fx_grp_name(self):
        if self.pinnacle_rx_data:
            return self.pinnacle_rx_data['fx_grp_name']
        return "FxGrp %s" % self.fx_grp_number

    @property
    def has_dose_ref(self):
        return hasattr(self.rt_plan, 'DoseReferenceSequence')

    @property
    def rx_dose(self):
        if self.pinnacle_rx_data:
            return self.pinnacle_rx_data['rx_dose']
        ans = self.get_dose_ref_attr('TargetPrescriptionDose')
        if ans is None:
            ans = float(self.dicompyler_plan['rxdose']) / 100.
        return ans

    @property
    def rx_percentage(self):
        if self.pinnacle_rx_data:
            return self.pinnacle_rx_data['rx_percentage']

    @property
    def fx_count(self):
        return int(self.fx_grp_data.NumberOfFractionsPlanned)

    @property
    def fx_dose(self):
        if self.pinnacle_rx_data:
            return self.pinnacle_rx_data['fx_dose']
        try:
            return round(self.rx_dose / float(self.fx_count), 2)
        except Exception as e:
            push_to_log(e, msg="RxParser: Unable to calculate fx_dose")

    @property
    def normalization_method(self):
        if self.pinnacle_rx_data:
            return self.pinnacle_rx_data['normalization_method']
        return self.get_dose_ref_attr('DoseReferenceStructureType')

    @property
    def normalization_object(self):
        if self.pinnacle_rx_data:
            return self.pinnacle_rx_data['normalization_object']
        if self.normalization_method:
            if self.normalization_method.lower() == 'coordinates':
                return 'COORDINATE'
            elif self.normalization_method.lower() == 'site':
                if hasattr(self.rt_plan, 'ManufacturerModelName'):
                    return self.rt_plan.ManufacturerModelName

    @property
    def beam_count(self):
        if hasattr(self.fx_grp_data, 'NumberOfBeams'):
            return int(self.fx_grp_data.NumberOfBeams)

    @property
    def beam_numbers(self):
        return [ref_beam.ReferencedBeamNumber for ref_beam in self.fx_grp_data.ReferencedBeamSequence]


class PreImportData:
    """
    Light-weight object for the DICOM Importer GUI to avoid memory allocation issues
    """
    def __init__(self, file_set, stored_values, dicompyler_rt_structures, roi_map=None):

        self.plan_file = file_set['plan']
        self.dose_file = file_set['dose']
        self.structure_file = file_set['structure']
        self.missing_files = [key.capitalize() for key, value in file_set.items() if value is None]

        self.stored_values = stored_values
        self.dicompyler_rt_structures = dicompyler_rt_structures
        self.database_rois = DatabaseROIs() if roi_map is None else roi_map

        # over ride objects
        keys = ['mrn', 'study_instance_uid', 'birth_date', 'sim_study_date', 'physician', 'tx_site', 'rx_dose']
        self.plan_over_rides = {key: None for key in keys}
        self.global_plan_over_rides = None

        self.roi_over_ride = {'name': {}, 'type': {}}

        # If importing with auto sum turned off, use this list to track plan-specific PTVs
        self.plan_ptvs = []

    @property
    def mrn(self):
        if self.plan_over_rides['mrn'] is not None:
            return self.plan_over_rides['mrn']
        return self.stored_values['mrn']

    @property
    def study_instance_uid(self):
        return self.stored_values['study_instance_uid_to_be_imported']

    @property
    def study_instance_uid_to_be_imported(self):
        if hasattr(self, 'plan_over_rides') and self.plan_over_rides['study_instance_uid']:
            return self.plan_over_rides['study_instance_uid']
        return self.stored_values['study_instance_uid_to_be_imported']

    @property
    def is_study_instance_uid_valid(self):
        return self.is_uid_valid(self.study_instance_uid)

    @property
    def is_study_instance_uid_to_be_imported_valid(self):
        return self.is_uid_valid(self.study_instance_uid_to_be_imported)

    @staticmethod
    def is_uid_valid(uid):
        valid = False
        if uid:
            with DVH_SQL() as cnx:
                valid = not cnx.is_study_instance_uid_in_table('Plans', uid)
        return valid

    @property
    def patient_name(self):
        return self.stored_values['patient_name']

    @property
    def file_set_complete(self):
        return all([self.plan_file, self.structure_file, self.dose_file])

    @property
    def rx_dose(self):
        if self.plan_over_rides['rx_dose'] is not None:
            ans = self.plan_over_rides['rx_dose']
        else:
            ans = self.stored_values['rx_dose']
        return self.process_global_over_ride('rx_dose', ans)

    @property
    def sim_study_date(self):
        if self.plan_over_rides['sim_study_date'] is not None:
            ans = self.plan_over_rides['sim_study_date']
        else:
            ans = self.stored_values['sim_study_date']
        return self.process_global_over_ride('sim_study_date', ans)

    @property
    def birth_date(self):
        if self.plan_over_rides['birth_date'] is not None:
            ans = self.plan_over_rides['birth_date']
        else:
            ans = self.stored_values['birth_date']
        return self.process_global_over_ride('birth_date', ans)

    @property
    def physician(self):
        if self.plan_over_rides['physician'] is not None:
            ans = self.plan_over_rides['physician']
        else:
            ans = self.stored_values['physician']
        return self.process_global_over_ride('physician', ans)

    @property
    def tx_site(self):
        if self.plan_over_rides['tx_site'] is not None:
            ans = self.plan_over_rides['tx_site']
        else:
            ans = self.stored_values['tx_site']
        return self.process_global_over_ride('tx_site', ans)

    @property
    def patient_orientation(self):
        return self.stored_values['patient_orientation']

    def process_global_over_ride(self, key, pre_over_ride_value):
        if self.global_plan_over_rides:
            over_ride = self.global_plan_over_rides[key]
            if over_ride['value']:
                if not over_ride['only_if_missing'] or (over_ride['only_if_missing'] and not pre_over_ride_value):
                    return over_ride['value']
        return pre_over_ride_value

    def get_roi_type(self, key):
        """
        Get the ROI type as defined in DICOM (e.g., PTV, ORGAN, EXTERNAL, etc.)
        :param key: index of ROI
        :type key: int
        :return: the roi type
        :rtype: str
        """

        roi_type_from_roi_map = self.database_rois.get_roi_type(self.physician, self.get_physician_roi(key))

        if key in list(self.roi_over_ride['type']):
            ans = self.roi_over_ride['type'][key]
        elif roi_type_from_roi_map != 'NONE':
            ans = roi_type_from_roi_map
        else:
            ans = self.dicompyler_rt_structures[key]['type'].upper()
        return ans if ans else 'NONE'

    def reset_roi_type_over_ride(self, key):
        self.roi_over_ride['type'][key] = None

    def get_roi_name(self, key):
        """
        Applies clean_name from roi_name_manager.py to the name in the DICOM file
        :param key: the index of the roi
        :return: roi name to be used in the database
        :rtype: str
        """
        if key in list(self.roi_over_ride['name']):
            return clean_name(self.roi_over_ride['name'][key])
        return clean_name(self.dicompyler_rt_structures[key]['name'])

    def set_roi_name(self, key, name):
        self.roi_over_ride['name'][key] = clean_name(name)

    def get_physician_roi(self, key):
        """
        Look up the physician roi of the specified roi for this plan
        :param key: the index of the roi
        :return: physician roi or 'uncategorized'
        :rtype: str
        """
        roi_name = self.get_roi_name(key)
        if self.database_rois.is_roi(roi_name):
            if self.database_rois.is_physician(self.physician):
                return self.database_rois.get_physician_roi(self.physician, roi_name)
        return 'uncategorized'

    def get_institutional_roi(self, key):
        """
        Look up the institutional roi of the specified roi for this plan
        :param key: the index of the roi
        :return: institutional roi or 'uncategorized'
        :rtype: str
        """
        roi_name = self.get_roi_name(key)
        if self.database_rois.is_roi(roi_name):
            if self.database_rois.is_physician(self.physician):
                return self.database_rois.get_institutional_roi(self.physician, self.get_physician_roi(key))
            if roi_name in self.database_rois.institutional_rois:
                return roi_name
        return 'uncategorized'

    @property
    def ptv_exists(self):
        """
        Check if the plan has at least one PTV assigned
        :rtype: bool
        """
        if self.dicompyler_rt_structures:
            for key in list(self.dicompyler_rt_structures):
                if self.get_roi_type(key) == 'PTV':
                    return True
        return False

    @property
    def roi_names(self):
        """
        :return: roi_names for this plan per the plan (clean_name not applied)
        :rtype: list
        """
        return [self.get_roi_name(key) for key in list(self.dicompyler_rt_structures)]

    def get_roi_key(self, roi_name):
        """
        Look-up the roi index for a given roi_name
        :param roi_name: the ROI name to be looked-up
        :return: the roi index or None
        :rtype: int
        """
        roi_name = clean_name(roi_name)
        for key in list(self.dicompyler_rt_structures):
            if roi_name == clean_name(self.get_roi_name(key)):
                return key

    @property
    def ptv_names(self):
        return self.stored_values['ptv_names']

    @property
    def init_param(self):
        params = ['plan_file', 'structure_file', 'dose_file', 'plan_ptvs',
                  'plan_over_rides', 'global_plan_over_rides', 'roi_over_ride']
        return {key: getattr(self, key) for key in params}

    @property
    def validation(self):
        """
        :return: data used in GUI to indicate validity of data read-in from DICOM files to attract user to edit data
        :rtype: dict
        """
        return {'physician': {'status': self.database_rois.is_physician(self.physician) and self.physician != 'DEFAULT',
                              'value': self.physician,
                              'message': "No physician assigned or physician is not in ROI Map."},
                'mrn': {'status': self.mrn is not None,
                        'value': self.mrn,
                        'message': "MRN is empty."},
                'study_instance_uid': {'status': self.is_study_instance_uid_to_be_imported_valid,
                                       'value': self.study_instance_uid_to_be_imported,
                                       'message': "Study Instance UID used in the database."},
                'ptv': {'status': self.ptv_exists,
                        'value': self.ptv_names,
                        'message': "No PTV found."},
                'sim_study_date': {'status': is_date(self.sim_study_date),
                                   'value': self.sim_study_date,
                                   'message': "Simulation date is empty or invalid."},
                'rx_dose': {'status': self.rx_dose is not None,
                            'value': self.rx_dose,
                            'message': "Prescription dose is not defined."},
                'complete_file_set': {'status': self.file_set_complete,
                                      'value': self.file_set_complete,
                                      'message': ["Missing RT %s." % ', '.join(self.missing_files), '']
                                      [self.file_set_complete]}}

    @property
    def warning(self):
        msg = ''
        incomplete = False
        if self.plan_file and self.dose_file and self.structure_file:
            validation = self.validation
            failed_keys = {key for key, value in validation.items() if not value['status']}
            if failed_keys:
                if 'complete_file_set' in failed_keys:
                    msg = "ERROR: %s" % validation['complete_file_set']['message']
                    incomplete = True
                else:
                    msg = "WARNING: %s" % ' '.join([validation[key]['message'] for key in failed_keys])
        else:
            msg = "ERROR: Incomplete Fileset. RT Plan, Dose, and Structure required."
            incomplete = True

        return {'label': msg, 'incomplete': incomplete}

    def autodetect_target_roi_type(self, key=None):
        """
        Target/tumor ROIs are often not labeled properly in ROI Type, but often start with correct acronym
        any ROI that starts with GTV, CTV, ITV, or PTV and is followed by nothing, a single number, or a character
        then a single number will be flagged.
        :param key: the index of the roi, if key is None, will search all keys
        """

        if key is None:
            roi_names = {key: structure['name'].lower() for key, structure in self.dicompyler_rt_structures.items()}
        else:
            roi_names = {key: self.dicompyler_rt_structures[key]['name'].lower()}

        targets = {'gtv', 'ctv', 'itv', 'ptv'}
        for key, roi_name in roi_names.items():
            roi_name_len = len(roi_name)
            if self.database_rois.get_roi_type(self.physician, roi_name) == 'NONE':
                if self.get_physician_roi(key).lower() in targets:
                    self.roi_over_ride['type'][key] = self.get_physician_roi(key).upper()
                elif (roi_name_len > 2 and roi_name[0:3] in targets) and \
                        ((roi_name_len == 3) or
                         (roi_name_len == 4 and roi_name[3].isdigit()) or
                         (roi_name_len == 5 and not roi_name[3].isdigit() and roi_name[4].isdigit())):
                    self.roi_over_ride['type'][key] = roi_name[0:3].upper()
