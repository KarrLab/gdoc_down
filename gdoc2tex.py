#!/usr/bin/env python

'''
gdoc2tex

Command line program to save the content of a Google document to a text file. The program
has one argument:
- Google document file name

The first time the program is called, the program will request access to the user's Google
account.

The program requires the google-api-python-client, oauth2client, PyOpenSSL packages. These
can be installed using pip:
>> pip install --upgrade google-api-python-client
>> pip install --upgrade oauth2client
>> pip install PyOpenSSL

Author: Jonathan Karr, karr@mssm.edu
Last updated: 2015-11-03
'''

from apiclient import discovery
import httplib2
import json
import re
import oauth2client
from oauth2client import client
from oauth2client import tools
import os
from os import path
import sys
   
CLIENT_SECRET_PATH = path.join(path.dirname(path.realpath(__file__)), 'client.json')
CREDENTIAL_PATH = path.join(path.dirname(path.realpath(__file__)), 'auth.json')
APPLICATION_NAME = 'gdoc2tex'
SCOPES = (
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
    )
    
def getTextRecursively(el):
    text = el.text or ''
    for child in list(el):
        text = text + getTextRecursively(child)
    return text

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    try:
        import argparse
        flags = tools.argparser.parse_args(args=[])
    except ImportError:
        flags = None
        
    store = oauth2client.file.Storage(CREDENTIAL_PATH)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_PATH, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
    return credentials

def main(argv):    
    ifile = argv[0]
    
    #authenticate
    credentials = get_credentials()
    http_auth = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http_auth)
    
    #get document id
    with open(ifile) as data_file:    
        data = json.load(data_file)
    gdoc_id = data['doc_id']
    
    #download file
    file = service.files().get(fileId=gdoc_id).execute()
    resp, content = service._http.request(file['exportLinks']['text/html'])
    
    #parse XML
    import xml.etree.ElementTree as ET
    
    content = content \
        .replace( \
            '<meta content="text/html; charset=UTF-8" http-equiv="content-type">', \
            '<meta content="text/html; charset=UTF-8" http-equiv="content-type"/>') \
        .replace('<hr style="page-break-before:always;display:none;">', '') \
        .replace("<br>",  "\n") \
        .replace("&nbsp;",  " ") \
        .replace("&Ooml;",  '\\"O ') \
        .replace("&ooml;",  '\\"o ') \
        .replace("&Uuml;",  '\\"U ') \
        .replace("&ouml;",  '\\"u ') \
        .replace("&mdash;",  '---') \
        .replace("&rsquo;", "'") \
        .replace("&sim;", "~")
    
    pattern = re.compile('<img.*?>')
    content = pattern.sub('', content)
            
    #local_fd = open(ifile.replace('.gdoc', '.xml'), "w")
    #local_fd.write(content)
    #local_fd.close()
            
    root = ET.fromstring(content)
    
    #inline comments
    comment_id = 0
    while True:
        comment_id = comment_id + 1
        comment = root.find((".//a[@name='cmnt%d']/../span" % comment_id))
        if comment is None:
            break
        root.find((".//a[@name='cmnt_ref%d']" % comment_id)).text = ('\pdfcomment{%s}' % comment.text)
        comment_parent = root.find((".//a[@name='cmnt%d']/../.." % comment_id))
        comment_grandparent = root.find((".//a[@name='cmnt%d']/../../.." % comment_id))
        comment_grandparent.remove(comment_parent)
        
    #remove head
    root.remove(root.find("./head"))    
        
    #
    text = ''
    for child in list(root.find('./body')):        
        text = text + getTextRecursively(child)
        text = text + "\n\n"
    
    content = ET.tostring(root)
    
    if resp.status == 200:
        local_fd = open(ifile.replace('.gdoc', '.tex'), "w")
        local_fd.write(text)
        local_fd.close()
        print('File saved')
    else:
        print('An error occurred: %s' % resp)
                 
if __name__ == '__main__':
    main(sys.argv[1:])