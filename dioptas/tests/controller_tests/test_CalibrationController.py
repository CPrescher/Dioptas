# -*- coding: utf-8 -*-

from tests.utility import QtTest
from mock import MagicMock
import os
import gc

from PyQt4 import QtGui, QtCore
from PyQt4.QtTest import QTest

from model.DioptasModel import DioptasModel
from controller.CalibrationController import CalibrationController
from widgets.CalibrationWidget import CalibrationWidget

unittest_path = os.path.dirname(__file__)
data_path = os.path.join(unittest_path, '../data')

# mocking the functions which will block the unittest for some reason...
QtGui.QApplication.processEvents = MagicMock()
QtGui.QProgressDialog.setValue = MagicMock()


class TestCalibrationController(QtTest):
    def setUp(self):
        self.model = DioptasModel()
        self.model.calibration_model._calibrants_working_dir = os.path.join(data_path, 'calibrants')
        self.model.calibration_model.integrate_1d = MagicMock()
        self.model.calibration_model.integrate_2d = MagicMock()

        self.calibration_widget = CalibrationWidget()
        self.working_dir = {}
        self.calibration_controller = CalibrationController(working_dir=self.working_dir,
                                                            widget=self.calibration_widget,
                                                            dioptas_model=self.model)

    def tearDown(self):
        del self.model
        gc.collect()

    def test_automatic_calibration(self):
        self.calibration_controller.load_img(os.path.join(data_path, 'LaB6_40keV_MarCCD.tif'))
        self.calibration_controller.search_peaks(1179.6, 1129.4)
        self.calibration_controller.search_peaks(1268.5, 1119.8)
        self.calibration_controller.widget.sv_wavelength_txt.setText('0.31')
        self.calibration_controller.widget.sv_distance_txt.setText('200')
        self.calibration_controller.widget.sv_pixel_width_txt.setText('79')
        self.calibration_controller.widget.sv_pixel_height_txt.setText('79')
        calibrant_index = self.calibration_widget.calibrant_cb.findText('LaB6')
        self.calibration_controller.widget.calibrant_cb.setCurrentIndex(calibrant_index)

        QTest.mouseClick(self.calibration_widget.calibrate_btn, QtCore.Qt.LeftButton)
        self.app.processEvents()
        self.model.calibration_model.integrate_1d.assert_called_once_with()
        self.model.calibration_model.integrate_2d.assert_called_once_with()
        self.assertEqual(QtGui.QProgressDialog.setValue.call_count, 15)

        calibration_parameter = self.model.calibration_model.get_calibration_parameter()[0]
        self.assertAlmostEqual(calibration_parameter['dist'], .1967, places=4)

    def test_loading_and_saving_of_calibration_files(self):
        self.calibration_controller.load_calibration(os.path.join(data_path, 'LaB6_40keV_MarCCD.poni'))
        self.calibration_controller.save_calibration(os.path.join(data_path, 'calibration.poni'))
        self.assertTrue(os.path.exists(os.path.join(data_path, 'calibration.poni')))
        os.remove(os.path.join(data_path, 'calibration.poni'))

    def test_selecting_configuration_updates_parameter_display(self):
        calibration1 = {
            'dist': 0.2,
            'poni1': 0.08,
            'poni2': 0.081,
            'rot1': 0.0043,
            'rot2': 0.002,
            'rot3': 0.001,
            'pixel1': 7.9e-5,
            'pixel2': 7.9e-5,
            'wavelength': 0.3344,
            'polarization_factor': 0.99
        }
        calibration2 = {
            'dist': 0.3,
            'poni1': 0.04,
            'poni2': 0.021,
            'rot1': 0.0053,
            'rot2': 0.002,
            'rot3': 0.0013,
            'pixel1': 7.4e-5,
            'pixel2': 7.6e-5,
            'wavelength': 0.31,
            'polarization_factor': 0.98
        }

        self.model.calibration_model.set_pyFAI(calibration1)
        self.model.add_configuration()
        self.model.calibration_model.set_pyFAI(calibration2)

        self.model.select_configuration(0)

        model_calibration = self.model.configurations[0].calibration_model.spectrum_geometry.getPyFAI()
        del model_calibration['splineFile']
        del model_calibration['detector']
        current_displayed_calibration = self.calibration_widget.get_pyFAI_parameter()
        del current_displayed_calibration['polarization_factor']
        self.assertEqual(model_calibration, current_displayed_calibration)

        self.model.select_configuration(1)
        model_calibration = self.model.configurations[1].calibration_model.spectrum_geometry.getPyFAI()
        del model_calibration['splineFile']
        del model_calibration['detector']
        current_displayed_calibration = self.calibration_widget.get_pyFAI_parameter()
        del current_displayed_calibration['polarization_factor']
        self.assertEqual(model_calibration, current_displayed_calibration)


        current_displayed_calibration = self.calibration_widget.get_pyFAI_parameter()


if __name__ == '__main__':
    unittest.main()
