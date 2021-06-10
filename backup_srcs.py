#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Monday - September 28 2020, 16:05:16

@author: Michele Svanera, University of Glasgow


crontab -e

# Weekly backup
0 20 * * 1 /usr/bin/python3 /home/micheles/Desktop/backup/backup_srcs.py

Usage:
* go to 'micheles-pc'
* crontab -e
* 25 19 * * 1 /usr/bin/python3 /path/to/backup_srcs.py

(sudo EDITOR=nano crontab -e)

'''


################################################################################################################
## Imports

from __future__ import division, print_function

import os, sys
import argparse
from os.path import join as opj
from time import strftime, localtime
from shutil import copyfile
import subprocess

import numpy as np
import logging
from datetime import timedelta
import time
import smtplib, ssl
from email.message import EmailMessage

sys.path.insert(0, '/analyse/Project0235/segmentator/src/')
from cerebrum7t_lib import python_utils


################################################################################################################
## Paths and Constants

Path_in = '/analyse/'
Proj_to_backup = ['Project0204','Project0233','Project0235']
Path_out = '/media/micheles/data/Backup/src_code/'
Files_to_keep = ['.py', '.m', '.sh', '.md', '.ipynb', 'what.txt']
Path_to_exclude = ['/analyse/Project0204/packages/']    # those folders are too big

# Email setup
HOST = 'smtp.gmail.com'
USER = 'your_account@gmail.com'
PWD = 'you_PSW'
TO = 'your_mail'


################################################################################################################
## Functions

        
def initialiseOutputFolder(out_folder,initial_desciption='backup_'):
    
    # Compose output name
    local_time_str = strftime("%Y-%m-%d %H:%M:%S", localtime())
    log_filename_with_time = (local_time_str.replace(':','-')).replace(' ','_')
    out_folder_complete = initial_desciption + log_filename_with_time
    out_folder_complete = out_folder_complete.replace('/','-')
    
    os.mkdir(out_folder + out_folder_complete)
    # out_folder_complete = checkAndCreateFolderOut(out_folder + out_folder_complete)

    return out_folder_complete


def findListOfSourceFiles(path_in):

    all_anat = []
    for root, _, files in os.walk(path_in):
        for i_file in files:
            all_anat.append(root + '/' + i_file)
    
    return sorted(list(np.unique(all_anat)))


################################################################################################################
## Main

begin_time = time.time()

# Create an out folder and a log with the date
path_out_folder = initialiseOutputFolder(Path_out)
log_filename = opj(Path_out, path_out_folder, path_out_folder + '.log')
log = python_utils.initialiseLogger(log_filename, 
                                    with_time=False,
                                    log_level=20)

# Report size of project folders
for i_proj in Proj_to_backup:
    cmd = 'du -sh ' + opj(Path_in, i_proj)
    result = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
    size = (result.stdout).decode("utf-8").split('\t')[0]
    log.info('Folder ' + i_proj + ', size: ' + size)

log.info('\n')

# For every project folder
all_files = []
for i_proj in Proj_to_backup:

    start_time = time.time()
    log.info('Scanning ' + i_proj + ' ...')
    
    # Find all the src code files: '.py', '.sh'
    all_files += findListOfSourceFiles(opj(Path_in,i_proj))

    log.info('done in: ' + str(timedelta(seconds=(time.time() - start_time))) + ' (days, hh:mm:ss.ms)')

# Keep only src code files
all_files = [i for i in all_files for j in Files_to_keep if i[-len(j):] == j]

# Remove temp files
all_files = [i for i in all_files if '/._' not in i]

# Remove file to exclude
all_files = [i for i in all_files for j in Path_to_exclude if j not in i]

# Log and start copying
log.info('Ready to backup ' + str(len(all_files)) + ' files.\n\n')

start_time = time.time()
for i_file in all_files:

    # Create the out folder with the same structure
    i_path_out = Path_out + path_out_folder + i_file
    if not os.path.exists(os.path.dirname(i_path_out)):
        os.makedirs(os.path.dirname(i_path_out))

    # Copy file
    if not os.path.exists(i_path_out):
        try:
            output = copyfile(i_file, i_path_out)
        except:
            log.warning('Could not copy ' + i_file)
        # log.info(output)

log.info('\n\n\n')
log.info('Copied files done in: ' + str(timedelta(seconds=(time.time() - start_time))) + ' (days, hh:mm:ss.ms)')

# Log the size of the backup
cmd = 'du -sh ' + (Path_out + path_out_folder)
result = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
size = (result.stdout).decode("utf-8").split('\t')[0]
log.info('Backup size: ' + size + '\n\n')

log.info('Backup done in: ' + str(timedelta(seconds=(time.time() - begin_time))) + ' (days, hh:mm:ss.ms)')
logging.shutdown()


#### Send the log via email

#  Create content
with open(log_filename, 'r') as fp:
    content = fp.read()

# Create mail message
msg = EmailMessage()
msg.set_content(content)
msg["Subject"] = 'Backup src code - ' + strftime("%Y-%m-%d %H:%M:%S", localtime())
msg["From"] = USER
msg["To"] = TO
context=ssl.create_default_context()

# Send the email via our own SMTP server.
with smtplib.SMTP(HOST, port=587) as smtp:
    smtp.starttls(context=context)
    smtp.login(msg["From"], PWD)
    smtp.send_message(msg)





