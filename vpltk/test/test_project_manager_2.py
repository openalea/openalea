import unittest

from openalea.core.path import path as Path
from openalea.vpltk.project import ProjectManager

pm = ProjectManager()

def get_data_dir():
    return Path(__file__).parent.abspath() / 'data'

def get_data(filename):
    return get_data_dir() / filename

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        # Create tmp dir
        pass

    # def test_load_project(self):
    #     project = pm.load('test_project_lpy', projectdir=get_data_dir())
    #
    #     with self.assertRaises(ValueError) as cm:
    #         project = pm.load('unexisting_project')
    #
    #     msg = "Project 'unexisting_project' doesn't exist"
    #     self.assertEqual(cm.exception.message, msg)

    def tearDown(self):
        pass
        # Delete tmp dir