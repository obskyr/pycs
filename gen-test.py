# -*- coding: UTF-8 -*-

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
    print word[0] + ': ' + str(word[1]) + " times,",

print "\n\nHow often people swore with each swear:"
for u in check.swears:
    print u + ': ' + str(check.swears[u]) + " times,",

print "\n\nHow often people spoke during each hour:"
for time in check.times:
    print str(time) + " o' clock: " + str(check.times[time]) + " lines, ",

superfile = open('output\\superoutput.txt', 'w')
superfile.write('')
superfile.close()
superfile = open('output\\superoutput.txt', 'a')
superfile.write("Total number of lines: " + str(check.totallines))
superfile.write("\n\nTotal number of lines by user:\n")
for u in check.linenums:
    superfile.write(u + ': ' + str(check.linenums[u]) + " lines, ")
superfile.write("\n\nUsers that never spoke, only used actions (and their number of lines):\n")
for u in check.actionsonly:
    superfile.write(u + ': ' + str(check.actionsonly[u]) + " lines, ")
superfile.write("\n\nTotal number of actions by user:\n")
for u in check.uactions:
    superfile.write(u + ': ' + str(check.uactions[u]) + " actions, ")
superfile.write("\n\nRandom lines from each user:")
for user in check.randomlines:
    superfile.write("\n\t" + user.encode('utf-8') + ": " + check.randomlines[user].encode('utf-8'))
superfile.write("\n\nMost common words in the channel, and how often they were used:\n")
for word in check.wordlist[:15]:
    superfile.write(word[0] + ': ' + str(word[1]) + " times, ")
superfile.write("\n\nHow often people swore with each swear:")
for u in check.swears:
    superfile.write('\n' + u + ':')
    for swear in check.swears[u]:
        superfile.write('\n\t' + swear.encode('utf-8') + ': ' + str(check.swears[u][swear]).encode('utf-8') + " times")
superfile.write("\n\nHow often people spoke during each hour:\n")
for time in check.times:
    superfile.write(str(time) + " o' clock: " + str(check.times[time]) + " lines, ")

superfile.close()
