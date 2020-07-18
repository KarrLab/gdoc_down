`gdoc-down` documentation
=========================

API and command line program to save Google documents, presentations, and worksheets in a local Google Drive / Backup & Sync
directory to to local files.

`gdoc-down` supports several formats:

* CSV (.csv)
* EPUB (.epub)
* Excel workbook (.xlsx)
* HTML (.html)
* Image (.png, .jpg, .svg)
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

`gdoc-down` also has special features for handling .gdoc files that contain LaTeX:

* `gdoc-down` ignores all images. This allows the user to place images inside the Google 
  document for convenience and to use \includegraphics to embed images in compile PDF files.
* `gdoc-down` will convert all Google document comments to PDF comments.
* `gdoc-down` ignores all page breaks.

The first time `gdoc-down` is called, `gdoc-down` will request access to the user's Google
account. This will create a client.json file in the users home directory (~/.gdoc_down/client.json).

Contents
--------

.. toctree::
   :maxdepth: 3
   :numbered:

   installation.rst
   overview.rst
   API documentation <source/modules.rst>
   about.rst
