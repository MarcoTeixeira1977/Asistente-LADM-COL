import nose2

from qgis import utils
from qgis.core import QgsExpression
from qgis.testing import (unittest,
                          start_app)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (get_gpkg_conn,
                                            import_asistente_ladm_col)
from asistente_ladm_col.utils.qgis_utils import QGISUtils
from asistente_ladm_col.logic.ladm_col.qgis_ladm_query import QGISLADMQuery

from asistente_ladm_col.tests.resources.expected_results.queries.qgis_ladm_basic_query_test_results import expected_result_ladm_basic_query
from asistente_ladm_col.tests.resources.expected_results.queries.qgis_ladm_legal_query_test_results import expected_result_ladm_legal_query
from asistente_ladm_col.tests.resources.expected_results.queries.qgis_ladm_physical_query_test_results import expected_result_ladm_physical_query
from asistente_ladm_col.tests.resources.expected_results.queries.qgis_ladm_economic_query_test_results import expected_result_ladm_economic_query
from asistente_ladm_col.tests.resources.expected_results.queries.qgis_ladm_property_record_card_query_test_results import expected_result_ladm_property_record_card_query
from asistente_ladm_col.config.expression_functions import (get_domain_code_from_value,
                                                            get_domain_value_from_code)


class TestGenericQueryManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import_asistente_ladm_col() # Import plugin
        cls.db_gpkg = get_gpkg_conn('test_ladm_col_queries_qpkg')

        # We can't use the restored database connection because the expression functions use the one in the plugin;
        # that's why we have to get the database connection and assign it to the plugin
        cls.plugin = utils.plugins["asistente_ladm_col"]  # Dict of active plugins
        cls.conn_manager = cls.plugin.conn_manager
        cls.conn_manager.set_db_connector_for_source(cls.db_gpkg)
        cls.qgis_utils = QGISUtils()

        result = cls.db_gpkg.test_connection()
        cls.assertTrue(result[0], 'The test connection is not working')
        cls.assertIsNotNone(cls.db_gpkg.names.T_ID_F, 'Names is None')
        cls.query_manager = QGISLADMQuery(cls.qgis_utils)

        # Maybe custom expression functions are not register in processing module
        QgsExpression.registerFunction(get_domain_code_from_value)
        QgsExpression.registerFunction(get_domain_value_from_code)

    def test_generic_query_manager_igac_basic_query(self):
        print("\nINFO: Validating basic info query from IGAC...")

        keywords = {'plot_t_ids': [831]}
        result = self.query_manager.get_igac_basic_info(self.db_gpkg, **keywords)
        self.assertTrue(expected_result_ladm_basic_query == result, 'The result obtained is not as expected: {} {}'.format(expected_result_ladm_basic_query, result))

    def test_generic_query_manager_igac_legal_query(self):
        print("\nINFO: Validating legal info query from IGAC...")

        keywords = {'plot_t_ids': [831]}
        result = self.query_manager.get_igac_legal_info(self.db_gpkg, **keywords)
        self.assertTrue(expected_result_ladm_legal_query == result, 'The result obtained is not as expected: {} {}'.format(expected_result_ladm_legal_query, result))

    def test_generic_query_manager_igac_property_record_card_query(self):
        print("\nINFO: Validating property record card info query from IGAC...")

        keywords = {'plot_t_ids': [831]}
        result = self.query_manager.get_igac_property_record_card_info(self.db_gpkg, **keywords)
        self.assertTrue(expected_result_ladm_property_record_card_query == result, 'The result obtained is not as expected: {} {}'.format(expected_result_ladm_property_record_card_query, result))

    def test_generic_query_manager_igac_physical_query(self):
        print("\nINFO: Validating physical info query from IGAC...")

        keywords = {'plot_t_ids': [831]}
        result = self.query_manager.get_igac_physical_info(self.db_gpkg, **keywords)
        self.assertTrue(expected_result_ladm_physical_query == result, 'The result obtained is not as expected: {} {}'.format(expected_result_ladm_physical_query, result))

    def test_generic_query_manager_ladm_economic_query(self):
        print("\nINFO: Validating economic info query from IGAC...")

        keywords = {'plot_t_ids': [831]}
        result = self.query_manager.get_igac_economic_info(self.db_gpkg, **keywords)
        self.assertTrue(expected_result_ladm_economic_query == result, 'The result obtained is not as expected: {} {}'.format(expected_result_ladm_economic_query, result))

    @classmethod
    def tearDownClass(cls):
        print('Close connection')
        cls.db_gpkg.conn.close()



if __name__ == '__main__':
    nose2.main()
