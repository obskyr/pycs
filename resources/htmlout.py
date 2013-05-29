# -*- coding: UTF-8 -*-

import sys
import os
from generate import *
import time

def timePercents(check):
    totaltimelines = float(sum(check.times.values()))
    time1 = (sum((x[1] for x in check.times_ordered[:6])) / totaltimelines) * 100
    time2 = (sum((x[1] for x in check.times_ordered[6:12])) / totaltimelines) * 100
    time3 = (sum((x[1] for x in check.times_ordered[12:18])) / totaltimelines) * 100
    time4 = (sum((x[1] for x in check.times_ordered[18:])) / totaltimelines) * 100
    return round(time1, 1), round(time2, 1), round(time3, 1), round(time4, 1)

def outputLogHTML(check, x):
    
    y = time.time()
    time1, time2, time3, time4 = timePercents(check)
    timeimagestr = """<span class="timewrap">
	<img src='resources/images/time/dawn.png' class='left' width='10px'><img src='resources/images/time/dawn.png' class='time' width='""" + str(int(time1 * 0.8)).encode('utf-8') + """%'>
	<span class="hovertime dawn">
		0 - 6: """ + str(time1).encode('utf-8') + """%
	</span>
</span>
<span class="timewrap">
	<img src='resources/images/time/morning.png' class='time' width='1px'><img src='resources/images/time/morning.png' class='time' width='""" + str(int(time2 * 0.8)).encode('utf-8') + """%'>
	<span class="hovertime morning">
		6 - 12: """ + str(time2).encode('utf-8') + """%
	</span>
</span>
<span class="timewrap">
	<img src='resources/images/time/day.png' class="time" width='1px'><img src='resources/images/time/day.png' class="time" width='""" + str(int(time3 * 0.8)).encode('utf-8') + """%'>
	<span class="hovertime day">
		12 - 18: """ + str(time3).encode('utf-8') + """%
	</span>
</span>
<span class="timewrap">
	<img src='resources/images/time/night.png' class='time' width='""" + str(int(time4 * 0.8)).encode('utf-8') + """%'><img src='resources/images/time/night.png' class='right' width='10px'>
	<span class="hovertime night">
		18 - 0: """ + str(time4).encode('utf-8') + """%
	</span>
</span>"""

    commonwordsleft = []
    commonwordsright= []
    for word, uses in check.wordlist[:10:2]:
        commonwordsleft.append(word.encode('utf-8') + ': ' + str(uses).encode('utf-8') + ' uses')
    for word, uses in check.wordlist[1:10:2]:
        commonwordsright.append(word.encode('utf-8') + ': ' + str(uses).encode('utf-8') + ' uses')
    commonwordsleft = '\n\t\t\t\t<div class="smallBR"></div>\n\t\t\t\t'.join(commonwordsleft)
    commonwordsright= '\n\t\t\t\t<div class="smallBR"></div>\n\t\t\t\t'.join(commonwordsright)
    superfile = open(pycspath + '\\output\\index.html', 'w')
    superfile.write("""
<!DOCTYPE HTML>
<link rel="stylesheet" type="text/css" href="resources/stylesheet.css">
<head>
    <title>
        """ + channelname + """ statistics
    </title>
</head>
<body>
    <div style="width: 100%;">
        <div class="left">
            <h1>
                User statistics <img src="resources/images/stat.png" class="icon">
            </h1>
            <p>""")
    for user, lines in check.linenums_top[:detailusers]:
        superfile.write('\n\t\t\t<div class="semibold">' + user.encode('utf-8') + '</div>\n\t\t\t<div class="smallBR"></div>\n\t\t\t<div class="stat">\n\t\t\t' + \
        str(lines).encode('utf-8') + ' lines &middot; ' + str(check.uactions[user]).encode('utf-8') +    \
        ' actions &middot; ' + str(check.numswears[user]).encode('utf-8') + ' swears\n<br>' +    \
        '"' + check.randomlines[user].encode('utf-8') + '"</div>\n\t\t\t<br>')
    if len(check.linenums_top[detailusers:]) > 0:
        superfile.write("""
            <div class="allusers-head">
                These users didn't speak that much:
            </div>
            <div class="allusers">
                """)
        for user, lines in check.linenums_top[detailusers:-1]:
            superfile.write(user.encode('utf-8') + ' - ' + str(lines).encode('utf-8') + ' &middot; ')
        superfile.write(check.linenums_top[-1][0].encode('utf-8') + ' - ' + str(check.linenums_top[-1][1]).encode('utf-8') + '\n\t\t\t</div>')
        superfile.write("""
            </div>""")
    superfile.write("""
        </div>
        <div class="right">
            <h1>
                <img src="resources/images/quote.png" class="icon"> Specifics
            </h1>
            <br>
            <center>
                <span class="comment">
                    Lines by time posted
                </span>
                <br>
                <br>
                """ + timeimagestr.encode('utf-8') + """
                <br>
                <br>
                <span class="comment">
                    Mouseover for details
                </span>
                <br>
                <br>
                Total number of lines in """ + channelname.encode('utf-8') + """:
                <span class="totallines">
                    """ + str(check.totallines).encode('utf-8') + """
                </span>
                <br>
                <br>
                <div class="smallBR"></div>
                <div class="semibold">
                    Most common words:
                </div>
                <br>
                <div class="left commonwords">
                    """ + commonwordsleft.encode('utf-8') + """
                </div>
                <div class="right commonwords">
                    """ + commonwordsright.encode('utf-8') + """
                </div>
            </center>
        </div>
        
<!-- HERE BEGINS FOOTER -->

        <div style="clear:both;"></div>
        <br>
        <div class="footer">
            <center>
                These statistics were generated in """ + str(round(y - x, 2)).encode('utf-8') + """ seconds.
                <br>
                <a href="https://github.com/LpSamuelm/pycs">
                    PYCS
                </a>
            </center>
        </div>
    </div>
</body>""")
    superfile.close()

if __name__ == '__main__':
    x = time.time()
    outputLogHTML(Logs(pycspath + "\\", ["testlog.log"], printprogress), x)
