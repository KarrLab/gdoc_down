import os
import shutil
import subprocess
import tempfile
import unittest


class TestGdocDown(unittest.TestCase):

    def setUp(self):
        # create temporary directory for downloaded files
        self.out_dir = tempfile.mkdtemp()

    def tearDown(self):
        # cleanup temporary directory
        shutil.rmtree(self.out_dir)

    def test_gdoc2tex(self):
        out_dir = self.out_dir

        # create temporary directory for tex file
        os.mkdir(os.path.join(out_dir, 'examples'))

        # download gdoc and save to tex file
        subprocess.check_call(['python', 'gdoc_down/gdoc2tex.py', '-o', out_dir, 'examples/example.gdoc'])

        # check that tex file downloaded
        self.assertTrue(os.path.isfile(os.path.join(out_dir, 'examples', 'example.tex')))

        # check that tex file has correct content
        with open(os.path.join(out_dir, 'examples', 'example.tex')) as file:
            self.assertEqual(file.read().strip(), 'gdoc-down example file')
