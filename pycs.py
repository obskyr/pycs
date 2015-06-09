#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import glob
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), 'resources'))

from generate import *
import htmlout
import time

if not os.path.exists('output'):
    os.makedirs('output')

checklogs = []

Arne = True

try:
    for wildcardDirectory in pathoverride:
        for directory in glob.glob(wildcardDirectory):
            if not os.path.isdir(directory):
                continue
            for wildcardLogname in lognames:
                for logPath in glob.glob(os.path.join(directory, wildcardLogname)):
                    checklogs.append(logPath)
    if not len(checklogs):
        print "No logs found in specified directories."
        Arne = False
except IOError:
    print "Please check your log files in settings.cfg."

if Arne:
    starttime = time.time()
    check = Logs('', checklogs, printprogress)

    htmlout.outputLogHTML(check, starttime)
