"""
Command line program to save the content of a Google document to a local file in several 
formats.

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2016-08-16
:Copyright: 2016, Karr Lab
:License: MIT
"""

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from gdoc_down.core import GDocDown

class BaseController(CementBaseController):
    """ Base controller for command line application """

    class Meta:
        label = 'base'
        description = "Download Google documents to local files in various formats"
        arguments = [
            (['gdoc_file'], dict(type=str, help='path to Google document')),
            (['--format', '-f'], dict(type=str, help='output format (docx, html, odft, pdf, rtf, tex, txt)', default='docx')),
            (['--out_path', '-o'], dict(type=str, help='path where Google document should be downloaded', default='.')),
            (['--extension', '-e'], dict(type=str, help='output extension', default=None)),
        ]

    @expose(hide=True)
    def default(self):
        args = self.app.pargs

        GDocDown(credentials=self.app.credentials).download(args.gdoc_file, format=args.format, out_path=args.out_path, extension=args.extension)


class App(CementApp):
    """ Command line application """

    class Meta:
        label = 'gdoc_down'
        base_controller = 'base'
        handlers = [BaseController]

    def __init__(self, credentials=None, **kwargs):
        super(App, self).__init__(**kwargs)
        self.credentials = credentials


def main():
    with App() as app:
        app.run()


if __name__ == "__main__":
    main()
