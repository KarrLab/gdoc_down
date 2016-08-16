[![PyPI package](https://img.shields.io/pypi/v/gdoc-down.svg)](https://pypi.python.org/pypi/gdoc-down)
[![Documentation](https://readthedocs.org/projects/gdoc-down/badge/?version=latest)](http://gdoc-down.readthedocs.org)
[![Test results](https://circleci.com/gh/KarrLab/gdoc-down.svg?style=shield)](https://circleci.com/gh/KarrLab/gdoc-down)
[![Test coverage](https://coveralls.io/repos/github/KarrLab/gdoc-down/badge.svg)](https://coveralls.io/github/KarrLab/gdoc-down)
[![Code analysis](https://codeclimate.com/github/KarrLab/gdoc-down/badges/gpa.svg)](https://codeclimate.com/github/KarrLab/gdoc-down)
[![License](https://img.shields.io/github/license/KarrLab/gdoc-down.svg)](LICENSE)

## `gdoc2text`
Command line program to save Google documents to text files. The program has two arguments:
* `-i` `-ifile`: path to Google document
* `-e` `-ext`: desired extension

The program will save the file with the same name and path as the Google document but with the desired extension.

For example:
`gdoc2text.py -i MyDoc.gdoc -e text` will place the content of `MyDoc` in `MyDoc.text`.

## `gdoc2tex`
Command line program to save Google documents to LaTeX files. The program has one argument:
* path to Google document

The program will save the file with the same name and path as the Google document but with the `.tex` extension.

The program has several special features for handling LaTeX files:
* The program will ignore all images. This allows the user to place images inside the Google document for convenience and to use `includegraphics` to embed images in compile PDF files.
* The program will convert all Google document comments to PDF comments.
* The program ignores all page breaks.

For example:
`gdoc2tex.py MyDoc.gdoc` will place the content of `MyDoc` in `MyDoc.tex`.
