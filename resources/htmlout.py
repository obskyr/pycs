# -*- coding: UTF-8 -*-

import sys
import os
from generate import *
import time

def outputLogHTML(check=None, starttime=None):
    x = starttime
    if starttime == None:
        x = time.time()
    if check == None:
        check = Logs('', [pycspath + '\\testlog.log'], True)
    y = time.time()
    superfile = open(pycspath + '\\output\\index.html', 'w')
    superfile.write('<!DOCTYPE HTML>\n<link rel="stylesheet" type="text/css" href="resources/stylesheet.css">\n<head><title>' + channelname.encode('utf-8') + ' statistics</title></head>\n<body><p>')
    superfile.close()
    superfile = open(pycspath + '\\output\\index.html', 'a')
    for user, lines in check.linenums_top:
        superfile.write('<div id="nick">' + user.encode('utf-8') + '</div><div id="smallBR">&nbsp;</div>\n<div id="stat">\n\t' +             \
        str(lines) + ' lines &middot; ' + str(check.uactions[user]).encode('utf-8') +    \
        ' actions &middot; ' + str(check.numswears[user]).encode('utf-8') + ' swears\n<br>' +    \
        '"' + check.randomlines[user].encode('utf-8') + '"</div>\n<br>')
    superfile.write('<br><font size="1">These statistics were generated in ' + str(round(y - x, 2)).encode('utf-8') + ' seconds.</p></body>')
        
    superfile.close()

if __name__ == '__main__':
    outputLogHTML()
