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

if os.name == 'nt':
    appdpath = os.environ['APPDATA']

if not [x for x in pathoverride if x.strip()]:
    for directory in logdirs:
        for ptest in logpaths:
            if os.path.exists(os.path.join(appdpath, directory, ptest)):
                lpath = ptest
                break
        else:
            print "No log directories found. Try using path override."
        for log in lognames:
            if os.path.exists(os.path.join(appdpath, directory, lpath, log)):
                checklogs.append(os.path.join(appdpath, directory, lpath, log))
else:
    try:
        for directory in pathoverride:
            for logname in lognames:
                if os.path.exists(os.path.join(directory, logname)):
                    checklogs.append(os.path.join(directory, logname))
        if not len(checklogs):
            print "No logs found in specified directories."
    except IOError:
        print "Please check your path override in settings.cfg."
starttime = time.time()
check = Logs('', checklogs, printprogress)

htmlout.outputLogHTML(check, starttime)
