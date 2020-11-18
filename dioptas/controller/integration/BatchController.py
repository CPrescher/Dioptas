from glob import glob
import os
from functools import partial

import numpy as np
import h5py
from PIL import Image
from qtpy import QtWidgets, QtCore, QtGui

from ...widgets.UtilityWidgets import open_file_dialog, open_files_dialog, save_file_dialog
# imports for type hinting in PyCharm -- DO NOT DELETE
from ...widgets.integration import IntegrationWidget
from ...model.DioptasModel import DioptasModel
from ...model.util.HelperModule import get_partial_index, get_partial_value


class BatchController(object):
    """
    The class manages the Image actions in the batch integration Window. It connects the file actions, as
    well as interaction with the image_view.
    """

    def __init__(self, widget, dioptas_model):
        """
        :param widget: Reference to IntegrationView
        :param dioptas_model: Reference to DioptasModel object

        :type widget: IntegrationWidget
        :type dioptas_model: DioptasModel
        """
        self.widget = widget
        self.model = dioptas_model

        self.clicks = 0
        self.rect = None
        self.scale = np.array

        self.create_signals()
        self.create_mouse_behavior()

        self.trim = 1

    def create_signals(self):
        """
        Creates all the connections of the GUI elements.
        """
        self.widget.batch_widget.load_btn.clicked.connect(self.load_data)
        self.widget.batch_widget.save_btn.clicked.connect(self.save_data)
        self.widget.batch_widget.integrate_btn.clicked.connect(self.integrate)
        self.widget.batch_widget.waterfall_btn.clicked.connect(self.waterfall_mode)
        self.widget.batch_widget.phases_btn.clicked.connect(self.toggle_show_phases)
        self.widget.batch_widget.view_3d_btn.clicked.connect(self.change_view)
        self.widget.batch_widget.view_2d_btn.clicked.connect(self.change_view)
        self.widget.batch_widget.view_f_btn.clicked.connect(self.change_view)
        self.widget.batch_widget.scale_log_btn.clicked.connect(self.change_scale)
        self.widget.batch_widget.scale_lin_btn.clicked.connect(self.change_scale)
        self.widget.batch_widget.scale_sqrt_btn.clicked.connect(self.change_scale)
        self.widget.batch_widget.background_btn.clicked.connect(self.subtract_background)
        self.widget.batch_widget.calc_bkg_btn.clicked.connect(self.extract_background)
        self.widget.batch_widget.autoscale_btn.clicked.connect(self.img_autoscale_btn_clicked)

        # set unit of x axis
        self.widget.batch_widget.tth_btn.clicked.connect(self.set_unit_tth)
        self.widget.batch_widget.q_btn.clicked.connect(self.set_unit_q)
        self.widget.batch_widget.d_btn.clicked.connect(self.set_unit_d)
        self.widget.pattern_q_btn.clicked.connect(self.set_unit_q)
        self.widget.pattern_tth_btn.clicked.connect(self.set_unit_tth)
        self.widget.pattern_d_btn.clicked.connect(self.set_unit_d)

        # work with filenames
        self.widget.img_filename_txt.editingFinished.connect(self.filename_txt_changed)
        self.widget.img_directory_txt.editingFinished.connect(self.directory_txt_changed)
        self.widget.img_directory_btn.clicked.connect(self.directory_txt_changed)

        # image navigation
        self.widget.batch_widget.step_series_widget.next_btn.clicked.connect(self.load_next_img)
        self.widget.batch_widget.step_series_widget.previous_btn.clicked.connect(self.load_prev_img)
        self.widget.batch_widget.step_series_widget.pos_txt.editingFinished.connect(self.load_given_img)
        self.widget.batch_widget.step_series_widget.start_txt.editingFinished.connect(self.set_range_img)
        self.widget.batch_widget.step_series_widget.stop_txt.editingFinished.connect(self.set_range_img)
        self.widget.batch_widget.step_series_widget.step_txt.editingFinished.connect(self.process_step)
        self.widget.batch_widget.step_series_widget.slider.valueChanged.connect(self.process_slider)

        # 3D navigation
        self.widget.batch_widget.m_color_btn.sigColorChanged.connect(self.set_marker_color)
        self.widget.batch_widget.surf_pg_layout.wheelEvent = self.wheel_event_3d
        self.widget.batch_widget.surf_pg_layout.keyPressEvent = self.key_pressed_3d

        self.widget.batch_widget.img_view.img_view_box.sigRangeChanged.connect(self.update_axes_range)
        self.model.configuration_selected.connect(self.update_gui)

    def create_mouse_behavior(self):
        """
        Creates the signal connections of mouse interactions
        """
        self.widget.batch_widget.img_view.mouse_moved.connect(self.show_img_mouse_position)
        self.widget.batch_widget.img_view.mouse_left_clicked.connect(self.img_mouse_click)

        self.widget.pattern_widget.mouse_left_clicked.connect(self.pattern_left_click)

    def set_marker_color(self):

        color = self.widget.batch_widget.m_color_btn.color(mode = 'float')
        print(color)
        self.widget.batch_widget.surf_view.marker_color = color[:3]
        self.plot_batch()

    def key_pressed_3d(self, ev):
        pressed_key = ev.key()
        self.widget.batch_widget.surf_view.pressed_key = pressed_key
        print("Key", pressed_key)
        if pressed_key == 49:
            self.widget.batch_widget.scale_lin_btn.setChecked(True)
            self.scale = np.array
        if pressed_key == 50:
            self.widget.batch_widget.scale_sqrt_btn.setChecked(True)
            self.scale = np.sqrt
        if pressed_key == 51:
            self.widget.batch_widget.scale_log_btn.setChecked(True)
            self.scale = np.log10
        if pressed_key == 66:
            if self.widget.batch_widget.background_btn.isChecked():
                self.widget.batch_widget.background_btn.setChecked(False)
            else:
                self.widget.batch_widget.background_btn.setChecked(True)
        if pressed_key == 72:
            self.widget.batch_widget.trim_h_btn.setChecked(True)
        if pressed_key == 76:
            self.widget.batch_widget.trim_l_btn.setChecked(True)
        if pressed_key == 88:
            self.widget.batch_widget.scale_x_btn.setChecked(True)
        if pressed_key == 89:
            self.widget.batch_widget.scale_y_btn.setChecked(True)
        if pressed_key == 90:
            self.widget.batch_widget.scale_z_btn.setChecked(True)
        if pressed_key == 83:
            self.widget.batch_widget.scale_s_btn.setChecked(True)
        if pressed_key == 71:
            self.widget.batch_widget.move_g_btn.setChecked(True)
        if pressed_key == 77:
            self.widget.batch_widget.move_m_btn.setChecked(True)
        #if pressed_key == 67:
        #    color_calc += 1
        #    if color_calc > 3:
        #        color_calc = 0

        self.plot_batch()



    def wheel_event_3d(self, ev):

        data = self.model.batch_model.data
        layout = self.widget.batch_widget.surf_pg_layout
        pressed_key = self.widget.batch_widget.surf_view.pressed_key
        show_range = self.widget.batch_widget.surf_view.show_range
        show_scale = self.widget.batch_widget.surf_view.show_scale
        surf_view = self.widget.batch_widget.surf_view

        delta = ev.angleDelta().x()
        if delta == 0:
            delta = ev.angleDelta().y()
        diff = delta / 10000

        if pressed_key == 72:
            if 1 > show_range[1] + diff > show_range[0]:
                show_range[1] += diff
        elif pressed_key == 76:
            if 0 < show_range[0] + diff < show_range[1]:
                show_range[0] += diff
        elif pressed_key == 88:
            show_scale[0] += diff
        elif pressed_key == 89:
            show_scale[1] += diff
        elif pressed_key == 90:
            show_scale[2] += diff
        elif pressed_key == 71:
            surf_view.g_translate += int(diff * data.shape[0] * 2)
        elif pressed_key == 77:
            if 0 <= surf_view.marker + int(diff * data.shape[1]) <= data.shape[1]:
                surf_view.marker += int(diff * data.shape[1])
        else:
            if ev.modifiers() & QtCore.Qt.ControlModifier:
                layout.opts['fov'] *= 0.999 ** delta
            else:
                layout.opts['distance'] *= 0.999 ** delta
            layout.update()

        self.plot_batch()



    def pattern_left_click(self, x, y):
        """
        Update position of vertical line

        :param x: Position of vertical line on pattern plot in current_configuration units
        """
        x = self.convert_x_value(x, self.model.current_configuration.integration_unit, '2th_deg')
        data_img_item = self.widget.batch_widget.img_view.data_img_item
        binning = self.model.batch_model.binning
        if binning is None:
            return
        bound = data_img_item.boundingRect().width()
        h_scale = (np.max(binning) - np.min(binning)) / bound
        h_shift = np.min(binning)
        pos = (x - h_shift)/h_scale

        self.widget.batch_widget.img_view.vertical_line.setValue(pos)

    def set_unit_tth(self):
        """
        Set 2th_deg unit on batch plot

        Corresponding buttons on batch and pattern widgets are checked.
        """
        self.widget.batch_widget.tth_btn.setChecked(True)
        self.widget.integration_pattern_widget.tth_btn.setChecked(True)
        self.model.current_configuration.integration_unit = '2th_deg'
        self.widget.batch_widget.img_view.bottom_axis_cake.setLabel(u'2θ', '°')
        self.widget.batch_widget.img_view.img_view_box.invertX(False)
        self.update_x_axis()

    def set_unit_q(self):
        """
        Set q_A^-1 unit on batch plot

        Corresponding buttons on batch and pattern widgets are checked.
        """
        self.widget.batch_widget.q_btn.setChecked(True)
        self.widget.integration_pattern_widget.q_btn.setChecked(True)
        self.model.current_configuration.integration_unit = "q_A^-1"
        self.widget.batch_widget.img_view.img_view_box.invertX(False)
        self.widget.batch_widget.img_view.bottom_axis_cake.setLabel('Q', 'A<sup>-1</sup>')
        self.update_x_axis()

    def set_unit_d(self):
        """
        Set d_A unit on batch plot

        Corresponding buttons on batch and pattern widgets are checked.
        """
        self.widget.batch_widget.d_btn.setChecked(True)
        self.widget.integration_pattern_widget.d_btn.setChecked(True)
        self.model.current_configuration.integration_unit = 'd_A'
        self.widget.batch_widget.img_view.bottom_axis_cake.setLabel('d', 'A')
        self.update_x_axis()

    def toggle_show_phases(self):
        """
        Show and hide phases
        """
        if str(self.widget.batch_widget.phases_btn.text()) == 'Show Phases':
            self.widget.batch_widget.img_view.show_all_visible_cake_phases(
                self.widget.phase_widget.phase_show_cbs)
            self.widget.batch_widget.phases_btn.setText('Hide Phases')
            self.model.enabled_phases_in_cake.emit()
        elif str(self.widget.batch_widget.phases_btn.text()) == 'Hide Phases':
            self.widget.batch_widget.img_view.hide_all_cake_phases()
            self.widget.batch_widget.phases_btn.setText('Show Phases')

    def subtract_background(self):
        """
        Toddle background subtraction in batch image
        """
        data = self.model.batch_model.data
        bkg = self.model.batch_model.bkg
        if data is None:
            return

        if bkg is None:
            self.widget.show_error_msg("Background is not jet calculated. Calculate background.")
            self.widget.batch_widget.background_btn.setChecked(False)
            return

        if data.shape != bkg.shape:
            self.widget.show_error_msg(f"Shape of data {data.shape} and background {bkg.shape} are different."
                                        "Recalculate background.")
            self.widget.batch_widget.background_btn.setChecked(False)
            return

        self.plot_batch()

    def extract_background(self):
        """
        Extract background from batch data
        """
        progress_dialog = self.widget.get_progress_dialog("Integrating multiple images.", "Abort Integration",
                                                          self.model.batch_model.n_img)

        parameters = self.widget.integration_control_widget.background_control_widget.get_bkg_pattern_parameters()
        self.model.batch_model.extract_background(parameters, progress_dialog)
        progress_dialog.close()

    def change_scale(self):
        """
        Change scale between log and linear
        """
        if self.widget.batch_widget.scale_log_btn.isChecked():
            self.scale = np.log10
        elif self.widget.batch_widget.scale_sqrt_btn.isChecked():
            self.scale = np.sqrt
        else:
            self.scale = np.array
        self.plot_batch()

    def process_step(self):
        """
        Re-draw waterfall plot if step value get changed.
        """
        if self.widget.batch_widget.waterfall_btn.isChecked():
            self.plot_waterfall()

    def waterfall_mode(self):
        """
        Set/unset widget in waterfall mode
        """
        if self.widget.batch_widget.waterfall_btn.isChecked():
            self.widget.batch_widget.img_view.vertical_line.setVisible(False)
            self.widget.batch_widget.img_view.horizontal_line.setVisible(False)
        else:
            if self.rect is not None:
                self.widget.batch_widget.img_view.img_view_box.removeItem(self.rect)
            self.widget.batch_widget.img_view.vertical_line.setVisible(True)
            self.widget.batch_widget.img_view.horizontal_line.setVisible(True)

    def process_slider(self):
        """
        Draw image if set values of image navigation widget if slider get changed
        """
        y = self.widget.batch_widget.step_series_widget.slider.value()
        x = self.widget.batch_widget.img_view.vertical_line.getXPos()
        self.widget.batch_widget.img_view.horizontal_line.setValue(y)
        self.load_single_image(x, y)

    def set_range_img(self):
        """
        Set start and stop value in the navigation widget
        """
        start = int(str(self.widget.batch_widget.step_series_widget.start_txt.text()))
        stop = int(str(self.widget.batch_widget.step_series_widget.stop_txt.text()))
        n_img_all = self.model.batch_model.n_img_all
        if n_img_all is None or stop < 0:
            return

        start = min(start, n_img_all, stop)
        stop = min(max(start, stop), n_img_all)

        self.set_navigation_range(None, (start, stop))
        self.plot_batch()

    def load_next_img(self):
        """
        Load next image in the batch
        """
        step = int(str(self.widget.batch_widget.step_series_widget.step_txt.text()))
        stop = int(str(self.widget.batch_widget.step_series_widget.stop_txt.text()))
        pos = int(str(self.widget.batch_widget.step_series_widget.pos_txt.text()))
        y = pos + step
        if y > stop:
            return
        x = self.widget.batch_widget.img_view.vertical_line.getXPos()
        self.widget.batch_widget.img_view.horizontal_line.setValue(y)
        self.load_single_image(x, y)

    def load_prev_img(self):
        """
        Load previous image in the batch
        """
        step = int(str(self.widget.batch_widget.step_series_widget.step_txt.text()))
        start = int(str(self.widget.batch_widget.step_series_widget.start_txt.text()))
        pos = int(str(self.widget.batch_widget.step_series_widget.pos_txt.text()))
        y = pos - step
        if y < start:
            return
        x = self.widget.batch_widget.img_view.vertical_line.getXPos()
        self.widget.batch_widget.img_view.horizontal_line.setValue(y)
        self.load_single_image(x, y)

    def load_given_img(self):
        """
        Load image given in the text box
        """
        pos = int(str(self.widget.batch_widget.step_series_widget.pos_txt.text()))
        x = self.widget.batch_widget.img_view.vertical_line.getXPos()
        self.widget.batch_widget.img_view.horizontal_line.setValue(pos)
        self.load_single_image(x, pos)

    def show_img_mouse_position(self, x, y):
        """
        Show position of the mouse with respect of the heatmap

        Show image number, position in diffraction pattern and intensity
        """
        img = self.model.batch_model.data
        binning = self.model.batch_model.binning
        y += int(str(self.widget.batch_widget.step_series_widget.start_txt.text()))

        if img is None or x > img.shape[1] or x < 0 or y > img.shape[0] or y < 0:
            return
        scale = (binning[-1] - binning[0]) / binning.shape[0]
        tth = x * scale + binning[0]
        z = img[int(y), int(x)]

        self.widget.batch_widget.mouse_pos_widget.cur_pos_widget.x_pos_lbl.setText(f'Img: {int(y):.0f}')
        self.widget.batch_widget.mouse_pos_widget.cur_pos_widget.y_pos_lbl.setText(f'2θ:{tth:.1f}')
        self.widget.batch_widget.mouse_pos_widget.cur_pos_widget.int_lbl.setText(f'{z:.1f}')

    def change_view(self):
        """
        Change between 2D, 3D and file views
        """
        if self.widget.batch_widget.view_f_btn.isChecked():
            self.widget.batch_widget.treeView.show()
            self.widget.batch_widget.img_pg_layout.hide()
            self.widget.batch_widget.surf_view.hide()
            self.widget.batch_widget.left_control_widget.hide()
            n_img_all = self.model.batch_model.n_img_all
            if n_img_all is not None:
                self.set_navigation_range((0, n_img_all-1), (0, n_img_all-1))
        elif self.widget.batch_widget.view_3d_btn.isChecked():
            self.widget.batch_widget.treeView.hide()
            self.widget.batch_widget.img_pg_layout.hide()
            self.widget.batch_widget.surf_view.show()
            self.widget.batch_widget.left_control_widget.show()
            self.plot_batch()
        else:
            n_img = self.model.batch_model.n_img
            if n_img is None:
                self.widget.batch_widget.view_f_btn.setChecked(True)
                return
            self.widget.batch_widget.treeView.hide()
            self.widget.batch_widget.img_pg_layout.show()
            self.widget.batch_widget.left_control_widget.hide()
            self.widget.batch_widget.surf_view.hide()
            self.set_navigation_range((0, n_img-1), (0, n_img-1))

    def filename_txt_changed(self):
        """
        Set image files of the batch base on filename given in the text box
        """
        current_filenames = self.model.batch_model.files
        if current_filenames is None:
            return
        current_directory = self.model.working_directories['image']

        img_filename_txt = str(self.widget.img_filename_txt.text())
        new_filenames = []
        for t in img_filename_txt.split():
            new_filenames += glob(os.path.join(current_directory, t))

        if len(new_filenames) > 0:
            try:
                self.load_raw_data(new_filenames)
            except TypeError:
                basenames = [os.path.basename(f) for f in current_filenames]
                self.widget.img_filename_txt.setText(' '.join(basenames))
        else:
            basenames = [os.path.basename(f) for f in current_filenames]
            self.widget.img_filename_txt.setText(' '.join(basenames))

    def directory_txt_changed(self):
        """
        Change directory name for image files of the batch
        """
        new_directory = str(self.widget.img_directory_txt.text())
        filenames = self.model.batch_model.files
        if filenames is None:
            return
        new_filenames = [os.path.join(new_directory, os.path.basename(f)) for f in filenames]
        self.load_raw_data(new_filenames)

    def load_data(self):
        """
        Set image files of the batch, base on files given in the dialog window
        """
        filenames = open_files_dialog(self.widget, "Load image data file(s)",
                                      self.model.working_directories['image'],
                                      ('Raw data (*.nxs *tif *tiff);;'
                                       'Proc data (*.nxs)')
                                      )

        if self.is_proc(filenames[0]):
            self.model.batch_model.reset_data()
            self.load_proc_data(filenames[0])
            self.load_raw_data(self.model.batch_model.files)
            self.widget.batch_widget.view_2d_btn.setChecked(True)
            self.change_view()
            self.plot_batch()
        else:
            self.widget.img_directory_txt.setText(os.path.dirname(filenames[0]))
            self.model.working_directories['image'] = os.path.dirname(filenames[0])
            self.model.batch_model.reset_data()
            self.load_raw_data(filenames)
            self.widget.batch_widget.view_f_btn.setChecked(True)
            self.change_view()

        self.plot_image(0)

    def is_proc(self, filename):
        """
        Check if file contains processed data
        """
        if os.path.splitext(filename)[1] == '.nxs':
            data_file = h5py.File(filename, "r")
            if 'data_type' in data_file.attrs and data_file.attrs['data_type'] == 'processed':
                return True
        return False

    def load_raw_data(self, filenames):
        """
        Load metadata for raw data

        Following information is loaded:
            filenames, number of images in each file
        """

        self.model.img_model.blockSignals(True)
        try:
            self.model.batch_model.set_image_files(filenames)
        except IOError:
            try:
                dir_name = self.model.working_directories['image']
                filenames = [os.path.join(dir_name, os.path.basename(f)) for f in filenames]
                self.model.batch_model.set_image_files(filenames)
            except IOError:
                print("Raw images are not found")

        self.model.img_model.blockSignals(False)
        files = self.model.batch_model.files
        file_map = self.model.batch_model.file_map
        self.widget.batch_widget.tree_model.clear()
        if files is not None:
            if len(file_map) == len(files):
                file_map = np.hstack((file_map, self.model.batch_model.data.shape[0]))
            self.widget.batch_widget.tree_model.setColumnCount(2)
            self.widget.batch_widget.tree_model.setHorizontalHeaderLabels(["Fine name", "N img"])
            self.widget.batch_widget.treeView.setColumnWidth(0, 400)
            for i, file in enumerate(files):
                self.widget.batch_widget.tree_model.appendRow(QtGui.QStandardItem(f"{file}"))
                self.widget.batch_widget.tree_model.setItem(i, 1,
                                                            QtGui.QStandardItem(f"{file_map[i + 1] - file_map[i]}"))

        n_img = self.model.batch_model.n_img
        n_img_all = self.model.batch_model.n_img_all
        self.widget.batch_widget.step_series_widget.pos_label.setText(f"Frame({n_img}/{n_img_all}):")

    def load_proc_data(self, filename):
        """
        Load processed data (diffraction patterns and metadata)
        """
        self.model.batch_model.load_proc_data(filename)
        self.widget.calibration_lbl.setText(
            self.model.calibration_model.calibration_name)

    def plot_batch(self, start=None, stop=None):
        """
        Plot batch of diffraction patters taking into account scale abd background subtraction
        """
        data = self.model.batch_model.data
        bkg = self.model.batch_model.bkg
        if data is None:
            return
        if self.widget.batch_widget.background_btn.isChecked():
            data = data - bkg
            data[data<0.1] = 0.1
        data = self.scale(data)

        if stop is None:
            stop = int(str(self.widget.batch_widget.step_series_widget.stop_txt.text()))
        if start is None:
            start = int(str(self.widget.batch_widget.step_series_widget.start_txt.text()))

        if self.widget.batch_widget.view_2d_btn.isChecked():
            self.widget.batch_widget.img_view.plot_image(data[start:stop + 1], True)
            self.widget.batch_widget.img_view.auto_level()
            self.update_y_axis()

        if self.widget.batch_widget.view_3d_btn.isChecked():
            self.widget.batch_widget.surf_view.plot_surf(data[start:stop + 1])
            self.widget.batch_widget.surf_view.update_scale(data[start:stop + 1])
            self.update_3d_axis(data[start:stop + 1])

    def save_data(self):
        """
        Save diffraction patterns and metadata
        """
        filename = save_file_dialog(self.widget, "Save Image.",
                                    os.path.join(self.model.working_directories['image']),
                                    ('Image (*.png);;Single file ascii (*csv);;'
                                     'Multifile ascii (*.xy *.chi *.dat);;'
                                     'GSAS (*.fxye);;Data (*nxs)'))

        name, ext = os.path.splitext(filename)
        if filename is not '':
            if ext == '.png':
                if self.widget.batch_widget.view_2d_btn.isChecked():
                    QtWidgets.QApplication.processEvents()
                    self.widget.batch_widget.img_view.save_img(filename)
            elif ext == '.nxs':
                self.model.batch_model.save_proc_data(filename)
            elif ext == '.csv':
                self.model.batch_model.save_as_csv(filename)
            else:
                self.model.img_model.blockSignals(True)
                img_data = self.model.batch_model.data
                pattern_x = self.model.batch_model.binning
                for y in range(img_data.shape[0]):
                    pattern_y = img_data[int(y)]
                    self.model.pattern_model.set_pattern(pattern_x, pattern_y)
                    self.model.current_configuration.save_pattern(f"{name}_{y}{ext}", subtract_background=True)
                self.model.img_model.blockSignals(False)

    def img_mouse_click(self, x, y):
        """
        Process mouse click
        """
        y += int(str(self.widget.batch_widget.step_series_widget.start_txt.text()))
        img = self.model.batch_model.data
        if img is None or x > img.shape[1] or x < 0 or y > img.shape[0] or y < 0:
            return
        if self.widget.batch_widget.waterfall_btn.isChecked():
            self.process_waterfall(x, y)
        else:
            self.load_single_image(x, y)

    def img_autoscale_btn_clicked(self):
        if self.widget.img_autoscale_btn.isChecked():
            self.widget.batch_widget.img_view.auto_level()

    def process_waterfall(self, x, y):
        """
        Create waterfall plot based on selected rectangle in the heatmap
        """
        # show overlay widget
        self.widget.integration_control_widget.tab_widget_1.setCurrentWidget(
            self.widget.integration_control_widget.overlay_control_widget
        )
        self.widget.integration_control_widget.tab_widget_2.setCurrentWidget(
            self.widget.integration_control_widget.overlay_control_widget
        )

        if self.clicks == 0:
            self.clicks += 1
            if self.rect is not None:
                self.widget.batch_widget.img_view.img_view_box.removeItem(self.rect)
            self.rect = self.widget.batch_widget.img_view.draw_rectangle(x, y)
            self.widget.batch_widget.img_view.mouse_moved.connect(self.rect.set_size)
            self.plot_pattern(int(x), int(y))
        elif self.clicks == 1:
            self.clicks = 0
            self.widget.batch_widget.img_view.mouse_moved.disconnect(self.rect.set_size)
            self.plot_waterfall()

    def plot_waterfall(self):
        """
        Create waterfall plot based on position and size of rectangle
        """
        data = self.model.batch_model.data
        binning = self.model.batch_model.binning
        rect = self.rect.rect()
        y1, y2 = sorted((int(rect.top()), int(rect.bottom())))
        x1, x2 = sorted((int(rect.left()), int(rect.right())))
        step = int(str(self.widget.batch_widget.step_series_widget.step_txt.text()))
        self.model.overlay_model.reset()
        new_binning = self.convert_x_value(binning[x1:x2], '2th_deg', self.model.current_configuration.integration_unit)
        for i in range(y1, y2, step):
            f_name, pos = self.model.batch_model.get_image_info(i)
            f_name = os.path.basename(f_name)
            self.model.overlay_model.add_overlay(new_binning, data[i, x1:x2], f'{f_name}, {pos}')
        separation = self.widget.integration_control_widget.overlay_control_widget.waterfall_separation_msb.value()
        self.model.overlay_model.overlay_waterfall(separation)

    def load_single_image(self, x, y):
        """
        Plot raw image, diffraction pattern and draw lines on the heatmap plot based on given x and y
        """
        self.plot_image(int(y))
        self.plot_pattern(int(x), int(y))

    def plot_pattern(self, x, y):
        """
        Plot diffraction pattern using proc data
        """
        img = self.model.batch_model.data
        binning = self.model.batch_model.binning
        if img is None or x > img.shape[1] or x < 0 or y > img.shape[0] or y < 0:
            return
        scale = (binning[-1] - binning[0]) / binning.shape[0]
        tth = x * scale + binning[0]
        z = img[y, x]

        self.widget.batch_widget.mouse_pos_widget.clicked_pos_widget.y_pos_lbl.setText(f'2θ:{tth:.1f}')
        self.widget.batch_widget.mouse_pos_widget.clicked_pos_widget.int_lbl.setText(f'I: {z:.1f}')
        new_binning = self.convert_x_value(binning, '2th_deg', self.model.current_configuration.integration_unit)
        self.model.pattern_model.set_pattern(new_binning, img[y])

    def plot_image(self, y):
        """
        Plot single raw image from the batch

        :param y: Number of raw image in the batch
        """
        y = int(y)
        self.model.current_configuration.auto_integrate_pattern = False
        self.model.batch_model.load_image(y, self.widget.batch_widget.view_f_btn.isChecked())
        f_name, pos = self.model.batch_model.get_image_info(y, self.widget.batch_widget.view_f_btn.isChecked())
        self.widget.batch_widget.setWindowTitle(f"Batch widget. {f_name} - {pos}")
        self.model.current_configuration.auto_integrate_pattern = True

        self.widget.batch_widget.step_series_widget.pos_txt.setText(str(y))
        self.widget.batch_widget.step_series_widget.slider.setValue(y)
        self.widget.batch_widget.mouse_pos_widget.clicked_pos_widget.x_pos_lbl.setText(f'Img: {y:.0f}')

    def update_axes_range(self):
        """
        Update axis of the 2D image
        """
        self.update_x_axis()
        self.update_y_axis()

    def update_3d_axis(self, data):
        if self.model.batch_model.binning is None:
            return

        surf_view = self.widget.batch_widget.surf_view
        binning = self.model.batch_model.binning
        h_scale = (np.max(binning) - np.min(binning)) / binning.shape[0]

        size = surf_view.pg_layout.pixelSize(np.array([0, 0, 0]))
        space = round(size * binning.shape[0] * 0.3, 2)
        print("sizeL: ", size, binning[0], binning[-1], round(size * binning.shape[0] * 0.2, 2), h_scale)
        # self.axis.set_tick_values(yticks=np.arange(0, data2.shape[1], 50000 * size))

        surf_view.axis.set_tick_values(yticks=np.round(np.arange(binning[0], binning[-1], space), 2))
        surf_view.g.setSpacing(np.nanmax(data)/8., space / h_scale, 1)
        surf_view.gx.setSpacing(1, space / h_scale, 1)

    def update_x_axis(self):
        if self.model.batch_model.binning is None:
            return

        data_img_item = self.widget.batch_widget.img_view.data_img_item
        binning = self.model.batch_model.binning

        width = data_img_item.viewRect().width()
        left = data_img_item.viewRect().left()
        h_scale = (np.max(binning) - np.min(binning)) / binning.shape[0]
        h_shift = binning[0]
        min_tth = h_scale * left + h_shift
        max_tth = h_scale * (left + width) + h_shift
        if self.model.current_configuration.integration_unit == 'q_A^-1':
            ticks = [self.get_ticks(max_tth, min_tth, 'q_A^-1', '2th_deg')]
        elif self.model.current_configuration.integration_unit == 'd_A':
            ticks = [self.get_ticks(min_tth, max_tth, 'd_A', '2th_deg')]
        else:
            ticks = None
        self.widget.batch_widget.img_view.bottom_axis_cake.setRange(min_tth, max_tth)
        self.widget.batch_widget.img_view.bottom_axis_cake.setTicks(ticks)

    def get_ticks(self, min_val, max_val, ticks_unit, base_unit, n_ticks=8):
        """
        Calculate ticks for x axis in case of non-linear scale
        """
        max_d = self.convert_x_value(max_val, base_unit, ticks_unit)
        min_d = self.convert_x_value(min_val, base_unit, ticks_unit)
        step = (max_d - min_d) / n_ticks
        x_d = min_d
        ticks = []
        while x_d > max_d:
            x_d = round(x_d + step, abs(round(np.log10(abs(step)))) + 1)
            x_tth = self.convert_x_value(x_d, ticks_unit, base_unit)
            ticks.append((x_tth, f"{x_d}"))
        return ticks

    def convert_x_value(self, value, previous_unit, new_unit):
        wavelength = self.model.calibration_model.wavelength
        if previous_unit == '2th_deg':
            tth = value
        elif previous_unit == 'q_A^-1':
            tth = np.arcsin(
                value * 1e10 * wavelength / (4 * np.pi)) * 360 / np.pi
        elif previous_unit == 'd_A':
            tth = 2 * np.arcsin(wavelength / (2 * value * 1e-10)) * 180 / np.pi
        else:
            tth = 0

        if new_unit == '2th_deg':
            res = tth
        elif new_unit == 'q_A^-1':
            res = 4 * np.pi * \
                  np.sin(tth / 360 * np.pi) / \
                  wavelength / 1e10
        elif new_unit == 'd_A':
            res = wavelength / (2 * np.sin(tth / 360 * np.pi)) * 1e10
        else:
            res = 0
        return res

    def update_y_axis(self):
        """
        Update y-axis of the batch plot
        """
        if self.model.batch_model.data is None:
            return

        start = int(str(self.widget.batch_widget.step_series_widget.start_txt.text()))
        stop = int(str(self.widget.batch_widget.step_series_widget.stop_txt.text()))

        data_img_item = self.widget.batch_widget.img_view.data_img_item
        img_data = self.model.batch_model.data[start:stop + 1]

        height = data_img_item.viewRect().height()
        bottom = data_img_item.viewRect().top()
        bound = data_img_item.boundingRect().height()

        v_scale = img_data.shape[0] / bound
        min_azi = v_scale * bottom + start
        max_azi = v_scale * (bottom + height) + start

        self.widget.batch_widget.img_view.left_axis_cake.setRange(min_azi, max_azi)

    def integrate(self):
        """
        Integrate images in the batch
        """
        if not self.model.calibration_model.is_calibrated:
            self.widget.show_error_msg("Can not integrate multiple images without calibration.")
            return
        if self.model.batch_model.n_img_all is None or self.model.batch_model.n_img_all < 1:
            self.widget.show_error_msg("No images loaded for integration")
            return

        if not self.widget.automatic_binning_cb.isChecked():
            num_points = int(str(self.widget.bin_count_txt.text()))
        else:
            num_points = None

        step = int(str(self.widget.batch_widget.step_series_widget.step_txt.text()))
        stop = int(str(self.widget.batch_widget.step_series_widget.stop_txt.text()))
        start = int(str(self.widget.batch_widget.step_series_widget.start_txt.text()))

        self.model.img_model.blockSignals(True)
        self.model.blockSignals(True)
        n_int = (stop-start)/step
        progress_dialog = self.widget.get_progress_dialog("Integrating multiple images.", "Abort Integration",
                                                          n_int)
        self.model.batch_model.integrate_raw_data(progress_dialog, num_points, start, stop + 1, step,
                                                  self.widget.batch_widget.view_f_btn.isChecked())
        progress_dialog.close()

        self.model.img_model.blockSignals(False)
        self.model.blockSignals(False)
        n_img = self.model.batch_model.n_img
        n_img_all = self.model.batch_model.n_img_all
        self.widget.batch_widget.view_2d_btn.setChecked(True)
        self.change_view()
        self.set_navigation_range((0, n_img-1), (0, n_img-1))
        self.widget.batch_widget.step_series_widget.pos_label.setText(f"Frame({n_img}/{n_img_all}):")
        self.plot_batch()

    def set_navigation_range(self, all_range, nav_range):
        """
        Set start and stop positions as well as range of navigation widget
        """
        if all_range is not None:
            self.widget.batch_widget.step_series_widget.start_txt.setRange(*all_range)
            self.widget.batch_widget.step_series_widget.stop_txt.setRange(*all_range)

        if nav_range is not None:
            self.widget.batch_widget.step_series_widget.slider.setRange(*nav_range)
            self.widget.batch_widget.step_series_widget.pos_validator.setRange(*nav_range)
            self.widget.batch_widget.step_series_widget.start_txt.setValue(nav_range[0])
            self.widget.batch_widget.step_series_widget.stop_txt.setValue(nav_range[1])

    def update_gui(self):
        """
        Apply integration unit from current_configuration
        """
        if self.model.current_configuration.integration_unit == '2th_deg':
            self.widget.batch_widget.tth_btn.setChecked(True)
            self.set_unit_tth()
        elif self.model.current_configuration.integration_unit == 'd_A':
            self.widget.batch_widget.d_btn.setChecked(True)
            self.set_unit_d()
        elif self.model.current_configuration.integration_unit == 'q_A^-1':
            self.widget.batch_widget.q_btn.setChecked(True)
            self.set_unit_q()
