import os
import sys

sys.path.insert(0, os.getcwd() + r"\resources")

import confutil
from generate import *

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
            if os.path.exists(appdpath + "\\" + directory + "\\" + ptest):
                lpath = ptest
                break
        else:
            print "No log directories found. Try using path override."
        for log in lognames:
            if os.path.exists(appdpath + "\\" + directory + "\\" + lpath + "\\" + log):
                checklogs.append(appdpath + "\\" + directory + "\\" + lpath + "\\" + log)
else:
    try:
        for directory in pathoverride:
            for logname in lognames:
                if os.path.exists(directory + "\\" + logname):
                    checklogs.append(directory + "\\" + logname)
        if not len(checklogs):
            print "No logs found in specified directories."
    except IOError:
        print "Please check your path override in settings.cfg."

check = Logs('', checklogs, printprogress)

print check.totallines
