`gdoc_down` documentation
=========================

API and command line program to save Google documents to local files in several formats:

* HTML (.html)
* LaTeX (.tex)
* Open document format (.odt)
* Plain text (.txt)
* Portable document format (.pdf)
* Rich text format (.rtf)
* Word documents (.docx)

The software has several special features for handling LaTeX files:

* The program ignores all images. This allows the user to place images inside the Google 
  document for convenience and to use `\includegraphics` to embed images in compile PDF files.
* The program will convert all Google document comments to PDF comments.
* The program ignores all page breaks.

The first time the program is called, the program will request access to the user's Google
account. This will create a client.json file in the users home directory (`~/.gdoc_down/client.json`).

Contents
--------

.. toctree::
   :maxdepth: 3

   installation.rst
   overview.rst
   API documentation <source/modules.rst>
   about.rst
