# -*- coding: UTF-8 -*-
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), 'resources'))

import confutil
from generate import *
import htmlout
import time

userdir = os.path.expanduser('~')
logpaths = ['logs', 'xchatlogs']

if not os.path.exists('output'):
    os.makedirs('output')

checklogs = []

Arne = True

try:
    for directory in pathoverride:
        for logname in lognames:
            if os.path.exists(os.path.join(directory, logname)):
                checklogs.append(os.path.join(directory, logname))
    if not len(checklogs):
        print "No logs found in specified directories."
        Arne = False
except IOError:
    print "Please check your log files in settings.cfg."

if Arne:
    starttime = time.time()
    check = Logs('', checklogs, printprogress)

    htmlout.outputLogHTML(check, starttime)
