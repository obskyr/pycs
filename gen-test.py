# -*- coding: cp1252 -*-

import sys
import os
sys.path.insert(0, os.getcwd() + "\\resources")
from generate import *

check = Logs('', ['testlog.log'], True)

print "Total number of lines:", check.totallines

print "\nTotal number of lines by user:"
for u in check.linenums:
    print u + ': ' + str(check.linenums[u]) + " lines,",

print "\n\nUsers that never spoke, only used actions (and their number of lines):"
for u in check.actionsonly:
    print u + ': ' + str(check.actionsonly[u]) + " lines,",

print "\n\nTotal number of actions by user:"
for u in check.uactions:
    print u + ': ' + str(check.uactions[u]) + " actions,",

print "\n\nRandom lines from each user:"
for user in check.randomlines:
    print '\t' + user + ': ' + check.randomlines[user]

print "\nMost common words in the channel, and how often they were used:"
for word in check.wordlist[:15]:
    print word[0] + ': ' + str(word[1]) + " times, ",

print "\n\nHow often people swore with each swear:"
for u in check.swears:
    print u + ': ' + str(check.swears[u]) + " times,",

print "\n\nHow often people spoke during each hour:"
for time in check.times:
    print str(time) + " o' clock: " + str(check.times[time]) + " lines, ",
