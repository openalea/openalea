import unittest

from openalea.vpltk.project import ProjectManager
pm = ProjectManager()


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        # Create tmp dir
        pass

    def test_load_project(self):
        project = pm.load('test_project_lpy', projectdir=get_test_data_dir())

        with self.assertRaises(ValueError) as cm:
            project = pm.load('unexisting_project')

        msg = "Project 'unexisting_project' doesn't exist"
        self.assertEqual(cm.exception.message, msg)

    def tearDown():
        # Delete tmp dir