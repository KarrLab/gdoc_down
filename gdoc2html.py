#!/usr/bin/env python

'''
gdoc2html

Command line program to save the content of a Google document to an HTML file. The program
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
import getopt
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
APPLICATION_NAME = 'gdoc2html'
SCOPES = (
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
    )

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
    odir = '.'
    try:
        opts, args = getopt.getopt(argv, "he:o:", ["ext=", "odir"])
    except getopt.GetoptError:
        print('gdoc2html.py -e <ext> -o <odir> <ifile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('gdoc2html.py -e <ext> -o <odir> <ifile>')
            sys.exit()
        elif opt in ("-e", "--ext"):
            ext = arg
        elif opt in ("-o", "--odir"):
            odir = arg
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
     
    if resp.status == 200:
        local_fd = open(os.path.join(odir, ifile.replace('.gdoc', '.docx')), "wb")
        local_fd.write(content)
        local_fd.close()
        print('File saved')
    else:
        print('An error occurred: %s' % resp)
                 
if __name__ == '__main__':
    main(sys.argv[1:])