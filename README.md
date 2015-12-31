# `gdoc2text`
Command line programs to save Google documents to text and LaTeX files.
* `gdoc2text`: saves Google documents to text files
* `gdoc2tex`: saves Google documents to LaTeX files

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

The program has two special features for handling LaTeX files:
* The program will ignore all images. This allows the user to place images inside the Google document for convenience and to use `includegraphics` to embed images in compile PDF files.
* The program will convert all Google document comments to PDF comments.

For example:
`gdoc2tex.py MyDoc.gdoc` will place the content of `MyDoc` in `MyDoc.tex`.
