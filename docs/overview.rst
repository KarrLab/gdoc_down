Command line usage
==================

.. code-block:: text

    gdoc-down (sub-commands ...) [options ...] {arguments ...}

    Download Google documents to local files in various formats

    positional arguments:
      gdoc_file             path to Google document

    optional arguments:
      -h, --help            show this help message and exit
      --debug               toggle debug output
      --quiet               suppress all output
      --format FORMAT, -f FORMAT
                            output format (docx, html, odft, pdf, rtf, tex, txt)
      --out_path OUT_PATH, -o OUT_PATH
                            path where Google document should be downloaded
      --extension EXTENSION, -e EXTENSION
                            output extension


Examples::

    gdoc-down -f docx /path/to/Google \Drive/file.gdoc
    gdoc-down -f pptx /path/to/Google \Drive/file.gslides
    gdoc-down -f xlsx /path/to/Google \Drive/file.gsheet
