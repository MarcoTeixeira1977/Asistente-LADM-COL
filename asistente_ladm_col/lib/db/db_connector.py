# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2017-11-20
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
import psycopg2

from qgis.PyQt.QtCore import QObject
from ...utils.model_parser import ModelParser
from ...config.enums import EnumTestLevel
from asistente_ladm_col.config.table_mapping_config import Names
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.config.general_config import (SUPPLIES_DB_MODEL,
                                                      SNR_DATA_DB_MODEL,
                                                      SUPPLIES_INTEGRATION_DB_MODEL,
                                                      OPERATION_DB_MODEL,
                                                      VALUATION_DB_MODEL,
                                                      CADASTRAL_FORM_DB_MODEL,
                                                      ANT_DB_MODEL,
                                                      REFERENCE_CARTOGRAPHY_DB_MODEL)

class DBConnector(QObject):
    """
    Superclass for all DB connectors.
    """

    _DEFAULT_VALUES = dict()

    def __init__(self, uri, conn_dict=dict()):
        QObject.__init__(self)
        self.logger = Logger()
        self.mode = ''
        self.provider = '' # QGIS provider name. e.g., postgres
        self._uri = None
        self.schema = None
        self.conn = None
        self._dict_conn_params = None
        self.names = Names()
        self.names_read = False  # Table/field names should be read only once per connector
        
        if uri is not None:
            self.uri = uri
        else:
            self.dict_conn_params = conn_dict

        self.model_parser = None

    @property
    def dict_conn_params(self):
        return self._dict_conn_params.copy()

    @dict_conn_params.setter
    def dict_conn_params(self, dict_values):
        dict_values = {k:v for k,v in dict_values.items() if v}  # To avoid empty values to overwrite default values
        self._dict_conn_params = self._DEFAULT_VALUES.copy()
        self._dict_conn_params.update(dict_values)
        self._uri = self.get_connection_uri(self._dict_conn_params, level=1)

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, value):
        raise NotImplementedError

    def equals(self, db):
        return self.dict_conn_params == db.dict_conn_params

    def test_connection(self, test_level=EnumTestLevel.LADM):
        raise NotImplementedError

    def validate_db(self):
        raise NotImplementedError

    def _get_table_and_field_names(self):
        raise NotImplementedError

    def close_connection(self):
        raise NotImplementedError

    def get_uri_for_layer(self, layer_name, geometry_type=None):
        raise NotImplementedError

    def get_description(self):
        return "Current connection details: '{}' -> {} {}".format(
            self.mode,
            self._uri,
            'schema:{}'.format(self.schema) if self.schema else '')

    def get_models(self, schema=None):
        raise NotImplementedError

    def get_logic_validation_queries(self):
        raise NotImplementedError

    def get_display_conn_string(self):
        # Do not use to connect to a DB, only for display purposes
        tmp_dict_conn_params = self._dict_conn_params.copy()
        if 'password' in tmp_dict_conn_params:
            del tmp_dict_conn_params['password']

        return ' '.join(["{}={}".format(k, v) for k, v in tmp_dict_conn_params.items()])

    def get_description_conn_string(self):
        raise NotImplementedError

    def get_connection_uri(self, dict_conn, level=1):
        """
        :param dict_conn: (dict) dictionary with the parameters to establish a connection
        :param level: (int) At what level the connection will be established
            0: server level
            1: database level
        :return: (str) string uri to establish a connection
        """
        raise NotImplementedError

    def operation_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.operation_model_exists()

        return False

    def valuation_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.valuation_model_exists()

        return False

    def cadastral_form_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.cadastral_form_model_exists()

        return False

    def ant_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.ant_model_exists()

        return False

    def ladm_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.ladm_model_exists()

        return False

    def reference_cartography_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.reference_cartography_model_exists()

        return False

    def snr_data_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.snr_data_model_exists()

        return False

    def supplies_integration_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.supplies_integration_model_exists()

        return False

    def supplies_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.supplies_model_exists()

        return False

    def required_models_exist(self, models):
        dict_required_models = dict()
        for model in models:
            if model == SUPPLIES_DB_MODEL:
                dict_required_models[SUPPLIES_DB_MODEL] = self.supplies_model_exists()
            if model == SNR_DATA_DB_MODEL:
                dict_required_models[SNR_DATA_DB_MODEL] = self.snr_data_model_exists()
            if model == SUPPLIES_INTEGRATION_DB_MODEL:
                dict_required_models[SUPPLIES_INTEGRATION_DB_MODEL] = self.supplies_integration_model_exists()
            if model == OPERATION_DB_MODEL:
                dict_required_models[OPERATION_DB_MODEL] = self.operation_model_exists()
            if model == VALUATION_DB_MODEL:
                dict_required_models[VALUATION_DB_MODEL] = self.valuation_model_exists()
            if model == CADASTRAL_FORM_DB_MODEL:
                dict_required_models[CADASTRAL_FORM_DB_MODEL] = self.cadastral_form_model_exists()
            if model == ANT_DB_MODEL:
                dict_required_models[ANT_DB_MODEL] = self.ant_model_exists()
            if model == REFERENCE_CARTOGRAPHY_DB_MODEL:
                dict_required_models[REFERENCE_CARTOGRAPHY_DB_MODEL] = self.reference_cartography_model_exists()

        return dict_required_models

    def read_model_parser(self):
        if self.model_parser is None:
            try:
                self.model_parser = ModelParser(self)
            except psycopg2.ProgrammingError as e:
                # if it is not possible to access the schema due to lack of privileges
                return False

        return True

    def is_ladm_layer(self, layer):
        raise NotImplementedError

    def get_ladm_layer_name(self, layer, validate_is_ladm=False):
        raise NotImplementedError

    def get_interlis_version(self):
        raise NotImplementedError