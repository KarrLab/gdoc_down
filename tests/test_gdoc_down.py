""" Tests gdoc_down

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2016-08-16
:Copyright: 2016, Karr Lab
:License: MIT
"""

from docx import Document as DocxDocument
from PyPDF2 import PdfFileReader
from gdoc_down.__main__ import App as cli
from gdoc_down.core import GDocDown
from oauth2client.client import GoogleCredentials
from odf import opendocument
from odf import text as odf_text
from xml.etree import ElementTree
import base64
import os
import sys
import shutil
import subprocess
import tempfile
import unittest

if sys.version_info < (3, 0, 0):
    import rtf2xml.ParseRtf


class TestGDocDown(unittest.TestCase):

    FIXTURE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'example.gdoc')

    def setUp(self):
        # create temporary directory for downloaded files
        self.out_dir = tempfile.mkdtemp()

        google_application_credentials_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'secret', 'GOOGLE_APPLICATION_CREDENTIALS')
        if os.getenv('GCLOUD_SERVICE_KEY'):
            secret_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'secret')
            if not os.path.isdir(secret_dir):
                os.makedirs(secret_dir)
            with open(google_application_credentials_path, 'wb') as file:
                file.write(base64.b64decode(os.getenv('GCLOUD_SERVICE_KEY')))
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_application_credentials_path
            self.credentials = GoogleCredentials.get_application_default()
        elif os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures', 'secret', 'GOOGLE_APPLICATION_CREDENTIALS')):
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_application_credentials_path
            self.credentials = GoogleCredentials.get_application_default()
        else:
            self.credentials = None

    def tearDown(self):
        # cleanup temporary directory
        shutil.rmtree(self.out_dir)

    def test_get_google_id(self):
        self.assertEqual(GDocDown.get_google_id(self.FIXTURE_FILE), '1mgPojZVReTAMBIVvt6LSQ59AGTsxx2-myLR9oIYIJ2s')

    def test_api_txt(self):
        GDocDown(credentials=self.credentials).download(self.FIXTURE_FILE,
                                                        format='txt', out_path=os.path.join(self.out_dir, 'example-out.text'))

        # check that file downloaded
        self.assertTrue(os.path.isfile(os.path.join(self.out_dir, 'example-out.text')))

        # check that file has correct content
        with open(os.path.join(self.out_dir, 'example-out.text'), 'r') as file:
            self.assertRegexpMatches(file.read().strip(), 'gdoc_down example file')

    def test_cli_2docx(self):
        with cli(argv=['-f', 'docx', '-o', self.out_dir, self.FIXTURE_FILE], credentials=self.credentials) as app:
            app.run()

        # check that file downloaded
        self.assertTrue(os.path.isfile(os.path.join(self.out_dir, 'example.docx')))

        # check that file has correct content
        doc = DocxDocument(os.path.join(self.out_dir, 'example.docx'))
        self.assertRegexpMatches(doc.paragraphs[0].text, 'gdoc_down example file')

    def test_cli_2html(self):
        with cli(argv=['-f', 'html', '-o', self.out_dir, self.FIXTURE_FILE], credentials=self.credentials) as app:
            app.run()

        # check that file downloaded
        self.assertTrue(os.path.isfile(os.path.join(self.out_dir, 'example.html')))

        # check that file has correct content
        with open(os.path.join(self.out_dir, 'example.html'), 'r') as file:
            self.assertRegexpMatches(file.read(), 'gdoc_down example file')

    def test_cli_2odt(self):
        with cli(argv=['-f', 'odt', '-o', self.out_dir, self.FIXTURE_FILE], credentials=self.credentials) as app:
            app.run()

        # check that file downloaded
        self.assertTrue(os.path.isfile(os.path.join(self.out_dir, 'example.odt')))

        # check that file has correct content
        doc = opendocument.load(os.path.join(self.out_dir, 'example.odt'))
        root = ElementTree.fromstring(doc.toXml().encode('utf-8'))
        self.assertRegexpMatches(GDocDown.get_element_text(root), 'gdoc_down example file')

    def test_cli_2pdf(self):
        with cli(argv=['-f', 'pdf', '-o', self.out_dir, self.FIXTURE_FILE], credentials=self.credentials) as app:
            app.run()

        # check that file downloaded
        self.assertTrue(os.path.isfile(os.path.join(self.out_dir, 'example.pdf')))

        # check that file has correct content
        with open(os.path.join(self.out_dir, 'example.pdf'), 'rb') as file:
            PdfFileReader(file)

    def test_cli_2rtf(self):
        with cli(argv=['-f', 'rtf', '-o', self.out_dir, self.FIXTURE_FILE], credentials=self.credentials) as app:
            app.run()

        # check that file downloaded
        self.assertTrue(os.path.isfile(os.path.join(self.out_dir, 'example.rtf')))

        # check that file has correct content
        if sys.version_info < (3, 0, 0):
            rtf2xml.ParseRtf.ParseRtf(
                in_file=os.path.join(self.out_dir, 'example.rtf'),
                out_file=os.path.join(self.out_dir, 'example.xml'),
            ).parse_rtf()

            root = ElementTree.parse(os.path.join(self.out_dir, 'example.xml'))
            self.assertRegexpMatches(GDocDown.get_element_text(root.getroot()), 'gdoc_down example file')

    def test_cli_2tex(self):
        with cli(argv=['-f', 'tex', '-o', self.out_dir, self.FIXTURE_FILE], credentials=self.credentials) as app:
            app.run()

        # check that file downloaded
        self.assertTrue(os.path.isfile(os.path.join(self.out_dir, 'example.tex')))

        # check that file has correct content
        with open(os.path.join(self.out_dir, 'example.tex'), 'r') as file:
            self.assertRegexpMatches(file.read().strip(), 'gdoc_down example file')

    def test_cli_2txt(self):
        with cli(argv=['-f', 'txt', '-o', self.out_dir, self.FIXTURE_FILE], credentials=self.credentials) as app:
            app.run()

        # check that file downloaded
        self.assertTrue(os.path.isfile(os.path.join(self.out_dir, 'example.txt')))

        # check that file has correct content
        with open(os.path.join(self.out_dir, 'example.txt'), 'r') as file:
            self.assertRegexpMatches(file.read().strip(), 'gdoc_down example file')
