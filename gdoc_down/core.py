"""
Save the content of a Google document, presentation, or workbook to a local file.

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2016-08-16
:Copyright: 2016, Karr Lab
:License: MIT
"""

from bs4 import BeautifulSoup
from xml.etree import ElementTree
import apiclient
import argparse
import io
import json
import re
import oauth2client
import oauth2client.tools
import os
import zipfile


class GDocDown(object):
    """ Downloads Google documents, presentations, and workbooks to several formats

    * CSV (.csv)
    * EPUB (.epub)
    * Excel workbook (.xlsx)
    * HTML (.html)
    * LaTeX (.tex)
    * Open Office document (.odt)
    * Open Office presentation (.odp)
    * Open Office workbook (.ods)
    * Plain text file (.txt)
    * Portable document format (.pdf)
    * Powerpoint presentation (.pptx)
    * Rich text document (.rtf)
    * TSV (.tsv)
    * Word document (.docx)

    The class has several special features for handling LaTeX files:

    * The program ignores all images. This allows the user to place images inside the Google
      document for convenience and to use \\\\includegraphics to embed images in compile PDF files.
    * The program will convert all Google document comments to PDF comments.
    * The program ignores all page breaks.

    The first time the program is called, the program will request access to the user's Google
    account. This will create a client.json file.

    Attributes:
        credentials (:obj:`oauth2client.client.OAuth2Credentials`): Credentials object for OAuth 2.0.
        service (:obj:`apiclient.discovery.Resource`): A Resource object with methods for interacting with the service
    """

    APPLICATION_NAME = 'gdoc_down'

    CLIENT_SECRET_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'client.json')

    CREDENTIAL_PATH = os.path.join(os.path.expanduser('~'), '.gdoc_down', 'auth.json')

    SCOPES = (
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive.metadata.readonly',
        'https://www.googleapis.com/auth/drive.readonly',
    )

    def __init__(self, credentials=None, service=None):
        """
        Arguments:
            credentials (:obj:`oauth2client.client.OAuth2Credentials`, optional): Credentials object for OAuth 2.0.
            service (:obj:`apiclient.discovery.Resource`, optional): A Resource object with methods for interacting with the service
        """
        if credentials is None:
            credentials = self.get_credentials()

        if service is None:
            service = self.authenticate(credentials)

        self.credentials = credentials
        self.service = service

    def get_credentials(self):
        """ Get and save user credentials from Google. If credentials haven't already been
        stored, or if the stored credentials are invalid, obtain the new credentials.

        Retuns:
            :obj:`oauth2client.client.OAuth2Credentials`: Credentials object for OAuth 2.0.
        """
        if not os.path.isdir(os.path.dirname(self.CREDENTIAL_PATH)):
            os.makedirs(os.path.dirname(self.CREDENTIAL_PATH))
        store = oauth2client.file.Storage(self.CREDENTIAL_PATH)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = oauth2client.client.flow_from_clientsecrets(self.CLIENT_SECRET_PATH, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            parser = argparse.ArgumentParser(
                description=__doc__,
                formatter_class=argparse.RawDescriptionHelpFormatter,
                parents=[oauth2client.tools.argparser])
            flags = parser.parse_args([])
            credentials = oauth2client.tools.run_flow(flow, store, flags)

        return credentials

    def authenticate(self, credentials):
        """ Authenticate with Google server

        Returns:
            :obj:`apiclient.discovery.Resource`: A Resource object with methods for interacting with the service
        """
        return apiclient.discovery.build('drive', 'v3', credentials=credentials)

    def download(self, google_file, format='docx', out_path='.', extension=None):
        """
        Args:
            google_file (:obj:`str`): path to Google document, presentation, or workbook
            format (:obj:`str`, optional): desired output format (docx, html, odt, pdf, rtf, tex, txt, etc)
            out_path (:obj:`str`, optional): path to save document, presentation, or workbook
            extension (:obj:`str`, optional): extension to document, presentation, or workbook

        Raises:
            obj:`Exception`: if format unknown or if ouput file path and extension cannot both be specified
        """

        _, google_file_ext = os.path.splitext(google_file)
        if google_file_ext == '.gdoc':
            if format == 'docx':
                export_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            elif format == 'epub':
                export_type = 'application/epub+zip'
            elif format == 'html':
                export_type = 'text/html'
            elif format == 'odt':
                export_type = 'application/vnd.oasis.opendocument.text'
            elif format == 'pdf':
                export_type = 'application/pdf'
            elif format == 'rtf':
                export_type = 'application/rtf'
            elif format == 'tex':
                export_type = 'application/zip'
            elif format == 'txt':
                export_type = 'text/plain'
            elif format == 'html.zip':
                export_type = 'application/zip'
            else:
                raise Exception('Unknown format "{}"'.format(format))
        elif google_file_ext == '.gsheet':
            if format == 'csv':
                export_type = 'text/csv'
            elif format == 'html.zip':
                export_type = 'application/zip'
            elif format == 'ods':
                export_type = 'application/x-vnd.oasis.opendocument.spreadsheet'
            elif format == 'pdf':
                export_type = 'application/pdf'
            elif format == 'tsv':
                export_type = 'text/tab-separated-values'
            elif format == 'xlsx':
                export_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            else:
                raise Exception('Unknown format "{}"'.format(format))
        elif google_file_ext == '.gslides':
            if format == 'odp':
                export_type = 'application/vnd.oasis.opendocument.presentation'
            elif format == 'pdf':
                export_type = 'application/pdf'
            elif format == 'pptx':
                export_type = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
            elif format == 'txt':
                export_type = 'text/plain'
            else:
                raise Exception('Unknown format "{}"'.format(format))
        else:
            raise Exception('Unknown Google document extension "{}"'.format(google_file_ext))

        if os.path.isdir(out_path):
            if extension is None:
                extension = format
            root, _ = os.path.splitext(os.path.basename(google_file))
            out_file = os.path.join(out_path, root + "." + extension)
        else:
            if extension is None or extension == os.path.splitext(out_path)[1][1:]:
                out_file = out_path
            else:
                raise Exception('Ouput file path and extension cannot both be specified')

        # get google document id
        google_id = self.get_google_id(google_file)

        # download file from Google
        content = self.service.files().export(fileId=google_id, mimeType=export_type).execute()

        # convert content as requested
        if format == 'txt':
            content = content[3:]
        elif format == 'tex':
            content = self.convert_html_to_latex(content)

        # save content to local file
        with open(out_file, "wb") as file:
            file.write(content)

    @classmethod
    def get_google_id(cls, google_file):
        """ Get Google document, presentation, or workbook id

        Args:
            google_file (:obj:`str`): path to Google document, presentation, or workbook

        Returns:
            :obj:`str`: id of Google document, presentation, or workbook
        """

        with open(google_file) as data_file:
            data = json.load(data_file)
        return data['doc_id']

    @classmethod
    def convert_html_to_latex(cls, html_zip_content):
        """ Format Google document content downloaded in HTML format for LaTeX

        * Replace HTML characters with LaTeX commands
        * Remove images
        * Replace comments with PDF comments (using `pdfcomment` package)

        Args:
            html_zip_content (:obj:`bytes`): HTML version of Google document

        Returns:
            :obj:`bytes`: formatted LaTeX
        """

        # recode html from zip file
        zip = zipfile.ZipFile(io.BytesIO(html_zip_content), 'r')
        filename = next(filename for filename in zip.namelist() if os.path.splitext(filename)[1] == '.html')
        html_content = zip.read(filename)

        # decode content
        html_content = html_content.decode('utf-8')

        """ remove unnecessary content """
        # head
        pattern = re.compile('<head>.*</head>')
        html_content = pattern.sub('', html_content)

        # style
        pattern = re.compile(' style=".*?"')
        html_content = pattern.sub('', html_content)

        # horizontal and break lines
        html_content = html_content \
            .replace('<hr style="page-break-before:always;display:none;">', '') \
            .replace("<br>",  "\n")

        # images
        pattern = re.compile('<img.*?>')
        html_content = pattern.sub('', html_content)

        """ substitute character entities """
        html_content = html_content.replace('&nbsp;', ' ')
        html_content = str(BeautifulSoup(html_content, 'html.parser'))

        """ replace comments with PDF comments (using `pdfcomment` package) """
        # parse html content
        root = ElementTree.fromstring(html_content)

        # find and replace comments: no longer exported by Google Drive
        """
        comment_id = 0
        while True:
            comment_id = comment_id + 1
            comment = root.find((".//a[@id='cmnt%d']" % comment_id))
            comment_parent = root.find((".//a[@id='cmnt%d']/.." % comment_id))
            comment_grandparent = root.find((".//a[@id='cmnt%d']/../.." % comment_id))
            comment_greatgrandparent = root.find((".//a[@id='cmnt%d']/../../.." % comment_id))
            if comment is None:
                break

            # remove numbering from comment
            comment_parent.remove(comment)

            # replace superscript with PDF comment
            ref = root.find((".//a[@id='cmnt_ref%d']" % comment_id))
            ref_parent = root.find((".//a[@id='cmnt_ref%d']/.." % comment_id))
            ref_parent.remove(ref)
            ref_parent.text = ('\pdfcomment{%s}' % cls.get_element_text(comment_grandparent))

            # remove comment footnote
            comment_greatgrandparent.remove(comment_grandparent)
        """

        # collect body text
        tex_content = ''
        for child in list(root.find('./body')):
            tex_content = tex_content + cls.get_element_text(child)
            tex_content = tex_content + "\n\n"

        """ return formatted LaTeX """
        return tex_content.encode('utf-8')

    @classmethod
    def get_element_text(cls, element):
        """ Get all of the text underneath an XML element

        Args:
            el (:obj:`xml.etree.ElementTree.Element`): XML element

        Returns:
            :obj:`str`: element's text
        """

        text = element.text or ''
        for child in list(element):
            text = text + cls.get_element_text(child)
        return text
