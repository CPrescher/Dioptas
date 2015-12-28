import unittest
import os
from PyQt4 import QtGui

from model.util.HelperModule import FileNameIterator

unittest_path = os.path.dirname(__file__)
data_path = os.path.join(unittest_path, 'data')


class FileNameIteratorTest(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.filename_iterator = FileNameIterator()

    def tearDown(self):
        del self.app

    def test_get_next_filename_with_existent_file(self):
        filename = 'image_001.tif'
        self.filename_iterator.update_filename(os.path.join(data_path, filename))
        new_filename = os.path.basename(self.filename_iterator.get_next_filename())
        self.assertEqual(new_filename, 'image_002.tif')

    def test_get_next_filename_with_non_existent_file(self):
        filename = 'image_002.tif'
        self.filename_iterator.update_filename(os.path.join(data_path, filename))
        self.assertEqual(self.filename_iterator.get_next_filename(), None)

    def test_get_next_filename_with_larger_Step(self):
        filename = 'image_000.tif'
        self.filename_iterator.update_filename(os.path.join(data_path, filename))
        new_filename = os.path.basename(self.filename_iterator.get_next_filename(step=2))
        self.assertEqual(new_filename, 'image_002.tif')

    def test_get_next_filename_with_two_numbers_in_name(self):
        filename1 = 'image_001w_001.tif'
        filename2 = 'image_002w_001.tif'
        file_path1 = os.path.join(data_path, filename1)
        file_path2 = os.path.join(data_path, filename2)

        open(file_path1, "w")
        open(file_path2, "w")

        self.filename_iterator.update_filename(file_path1)
        new_filename = self.filename_iterator.get_next_filename()
        self.assertEqual(new_filename, file_path2)

        os.remove(file_path1)
        os.remove(file_path2)

        filename1 = 'image_003w_001.tif'
        filename2 = 'image_003w_002.tif'
        filename3 = 'image_004w_001.tif'

        file_path1 = os.path.join(data_path, filename1)
        file_path2 = os.path.join(data_path, filename2)
        file_path3 = os.path.join(data_path, filename3)

        open(file_path1, "w")
        open(file_path2, "w")
        open(file_path3, "w")

        self.filename_iterator.update_filename(file_path1)
        new_filename = self.filename_iterator.get_next_filename()
        self.assertEqual(new_filename, file_path2)

        os.remove(file_path1)
        os.remove(file_path2)
        os.remove(file_path3)

    def test_get_previous_filename_with_existent_file(self):
        filename = 'image_002.tif'
        self.filename_iterator.update_filename(os.path.join(data_path, filename))
        new_filename = os.path.basename(self.filename_iterator.get_previous_filename())
        self.assertEqual(new_filename, 'image_001.tif')

    def test_get_previous_filename_with_non_existent_file(self):
        filename = 'image_001.tif'
        self.filename_iterator.update_filename(os.path.join(data_path, filename))
        self.assertEqual(self.filename_iterator.get_previous_filename(), None)

    def test_get_previous_filename_with_larger_Step(self):
        filename = 'image_003.tif'
        self.filename_iterator.update_filename(os.path.join(data_path, filename))
        new_filename = os.path.basename(self.filename_iterator.get_previous_filename(step=2))
        self.assertEqual(new_filename, 'image_001.tif')
