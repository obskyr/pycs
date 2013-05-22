# -*- coding: UTF-8 -*-

import sys
import os
sys.path.insert(0, os.getcwd() + "\\resources")
from generate import *
import time

x = time.time()
check = Logs('', ['testlog.log'], True)
y = time.time()
superfile = open('output\\index.html', 'w')
superfile.write('<!DOCTYPE HTML>\n<link rel="stylesheet" type="text/css" href="stylesheet.css">\n<head><title>' + channelname + ' statistics</title></head>\n<p>')
superfile.close()
superfile = open('output\\index.html', 'a')
superfile.write("Total number of lines: " + str(check.totallines))
superfile.write("<br>\n<br>\nTotal number of lines by user:<br>\n")
for u in check.linenums_top[:1]:
    superfile.write(u[0] + ': ' + str(u[1]) + " lines, ")
superfile.write("<br>\n<br>\nUsers that never spoke, only used actions (and their number of lines):<br>\n")
last = len(check.actionsonly) - 1
for i, u in enumerate(check.actionsonly):
    if i == last:
        superfile.write(u + ': ' + str(check.actionsonly[u]) + " lines")
        break
    superfile.write(u + ': ' + str(check.actionsonly[u]) + " lines, ")
superfile.write("<br>\n<br>\nTotal number of actions by user:<br>\n")
last = len(check.uactions) - 1
for i, u in enumerate(check.uactions):
    if i == last:
       superfile.write(u + ': ' + str(check.uactions[u]) + " actions")
       break
    superfile.write(u + ': ' + str(check.uactions[u]) + " actions, ")
superfile.write("<br>\n<br>\nRandom lines from each user:")
for user in check.randomlines:
    superfile.write("<br>\n  " + user.encode('utf-8') + ": " + check.randomlines[user].encode('utf-8'))
superfile.write("<br>\n<br>\nMost common words in the channel, and how often they were used:<br>\n")
for word in check.wordlist[:14]:
    superfile.write(word[0] + ': ' + str(word[1]) + " times, ")
superfile.write(check.wordlist[14][0] + ': ' + str(check.wordlist[14][1]) + " times")
superfile.write("<br>\n<br>\nHow often people swore with each swear:")
for u in check.swears:
    superfile.write('<br>\n<br>\n' + u + ':')
    for swear in check.swears[u]:
        superfile.write('<br>\n\t&emsp;' + swear.encode('utf-8') + ': ' + str(check.swears[u][swear]).encode('utf-8') + " times")
superfile.write("<br>\n<br>\nHow often people spoke during each hour:<br>\n")
for time in check.times_ordered[:-1]:
    superfile.write(str(time[0]) + " o' clock: " + str(time[1]) + " lines, ")
superfile.write(str(check.times_ordered[-1][0]) + " o' clock: " + str(check.times_ordered[-1][1]) + " lines")
superfile.write('<br><br><font size="1">These statistics were generated in ' + str(round(y - x, 2)).encode('utf-8') + " seconds.</font></p>")

superfile.close()
