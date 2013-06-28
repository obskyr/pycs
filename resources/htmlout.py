# -*- coding: UTF-8 -*-

import sys
import os
from generate import *
import time
import distutils.core
from filecmp import dircmp
import re


##

usernumberre    = re.compile("%usernumber%" )
usernamere      = re.compile("%username%"   )
linenumsre      = re.compile("%linenums%"   )
actionnumsre    = re.compile("%actionnums%" )
randomlinere    = re.compile("%randomline%" )

channelnamere   = re.compile("%channelname%")
gentimere       = re.compile("%gentime%"    )

dawnpre         = re.compile("%dawnpercent%"        )
morningpre      = re.compile("%morningpercent%"     )
daypre          = re.compile("%daypercent%"         )
nightpre        = re.compile("%nightpercent%"       )

dawnpnumre       = re.compile("%dawnpercent-([0-9]+)%"     )
morningpnumre    = re.compile("%morningpercent-([0-9]+)%"  )
daypnumre        = re.compile("%daypercent-([0-9]+)%"      )
nightpnumre      = re.compile("%nightpercent-([0-9]+)%"    )

totallinesre    = re.compile("%totallines%" )
swearnumre      = re.compile("%swears%"     )

userstatsre     = re.compile("\[userstats\](.*)\[/userstats\]", re.DOTALL               )
userstatslastre = re.compile("\[userstats-last\](.*)\[/userstats-last\]", re.DOTALL     )
swearsre        = re.compile("\[swears\].*\[/swears\]", re.DOTALL                       )
allusersre      = re.compile("\[allusers\](.*)\[/allusers\]", re.DOTALL                 )
allusersSre     = re.compile("\[allusers-section\](.*)\[/allusers-section\]", re.DOTALL )
alluserslastre  = re.compile("\[allusers-last\](.*)\[/allusers-last\]", re.DOTALL       )
alluserslasttagre = re.compile("\[/?allusers-last\]"                                    )
allusersStagre  = re.compile("\[/?allusers-section\]"                                   )
swearstagre     = re.compile("\[/?swears\]"                                             )

cwre            = re.compile("\[commonwords\](.*)\[/commonwords\]", re.DOTALL           )
cwoddre         = re.compile("\[commonwords-odd\](.*)\[/commonwords-odd\]", re.DOTALL   )
cwevenre        = re.compile("\[commonwords-even\](.*)\[/commonwords-even\]", re.DOTALL )

cwlastre        = re.compile("\[commonwords-last\](.*)\[/commonwords-last\]", re.DOTALL )
cwoddlastre     = re.compile("\[commonwords-odd-last\](.*)\[/commonwords-odd-last\]", re.DOTALL     )
cwevenlastre    = re.compile("\[commonwords-even-last\](.*)\[/commonwords-even-last\]", re.DOTALL   )

wordre          = re.compile("%word%"       )
usesre          = re.compile("%uses%"       )
numberre        = re.compile("%number%"     )

##

def timePercents(check):
    totaltimelines = float(sum(check.times.values()))
    time1 = (sum((x[1] for x in check.times_ordered[:6])) / totaltimelines) * 100
    time2 = (sum((x[1] for x in check.times_ordered[6:12])) / totaltimelines) * 100
    time3 = (sum((x[1] for x in check.times_ordered[12:18])) / totaltimelines) * 100
    time4 = (sum((x[1] for x in check.times_ordered[18:])) / totaltimelines) * 100
    return round(time1, 1), round(time2, 1), round(time3, 1), round(time4, 1)

def subSection(s, t):
    """Returns string 's' with all items in list 't' being re.sub'd - first element is pattern, second is replacement."""
    for pattern, replacement in t:
        s = re.sub(pattern, replacement, s)
    return s

def generateHTML(html, check, starttime):
    y = time.time()

    time1, time2, time3, time4 = timePercents(check)
    dawnpercent, morningpercent, daypercent, nightpercent = [str(x) for x in (time1, time2, time3, time4)]

    html = re.sub(channelnamere     , channelname   , html)
    html = re.sub(gentimere         , str(round(y - starttime, 2)), html)

    html = re.sub(dawnpre           , dawnpercent   , html)
    html = re.sub(morningpre        , morningpercent, html)
    html = re.sub(daypre            , daypercent    , html)
    html = re.sub(nightpre          , nightpercent  , html)

    dawnf       = lambda x: str(round(time1 * (float(x.group(1)) / 100), 1))
    morningf    = lambda x: str(round(time2 * (float(x.group(1)) / 100), 1))
    dayf        = lambda x: str(round(time3 * (float(x.group(1)) / 100), 1))
    nightf      = lambda x: str(round(time4 * (float(x.group(1)) / 100), 1))

    html = re.sub(dawnpnumre         , dawnf    , html)
    html = re.sub(morningpnumre      , morningf , html)
    html = re.sub(daypnumre          , dayf     , html)
    html = re.sub(nightpnumre        , nightf   , html)

    html = re.sub(totallinesre, str(check.totallines), html)

    usertop = list(enumerate(check.linenums_top))

    if not swearcount:
        html = re.sub(swearsre, "", html)
        html = re.sub(swearre, "", html)
    lasty = ""
    if re.search(userstatsre, html):
        endl = -1 if (re.search(userstatslastre, html)) else detailusers
        userstats = re.search(userstatsre, html).group(1)
        userstatsstr = []
        for number, pair in usertop[:detailusers][:endl]:
            user = pair[0]

            sublist = ((usernumberre, str(number)),
                       (usernamere, user),
                       (linenumsre, str(pair[1])),
                       (actionnumsre, str(check.uactions[user])),
                       (randomlinere, check.randomlines[user].replace('<', '&lt;').replace('>', '&gt;')),
                       (swearnumre, str(check.numswears[user])),
                       (swearstagre, "")
                       )
            userstatstemp = userstats
            userstatstemp = subSection(userstatstemp, sublist)
            userstatsstr.append(userstatstemp)
        if endl == -1:
            userstatslast = re.search(userstatslastre, html).group(1)
            user, number = usertop[:detailusers][endl][1][0], usertop[:detailusers][endl][0]
            sublist = ((usernumberre, str(number)),
                       (usernamere, user),
                       (linenumsre, str(pair[1])),
                       (actionnumsre, str(check.uactions[user])),
                       (randomlinere, check.randomlines[user].replace('<', '&lt;').replace('>', '&gt;')),
                       (swearnumre, str(check.numswears[user])),
                       (swearstagre, "")
                       )
            userstatstemp = userstatslast
            userstatstemp = subSection(userstatstemp, sublist)
            html = re.sub(userstatslastre, userstatstemp.encode('utf-8'), html)         
        userstatsstr = u''.join(userstatsstr).encode('utf-8')
    else:
        userstatsstr = ''
    html = re.sub(userstatsre, userstatsstr, html)
    if re.search(allusersre, html):
        endl = -1 if (re.search(alluserslasttagre, html)) else len(check.linenums_top)
        allusersstr = []
        allusers = re.search(allusersre, html).group(1)
        for number, pair in usertop[detailusers:endl]:
            user = pair[0]
            sublist =     ((usernumberre, str(number)),
                           (usernamere, user),
                           (linenumsre, str(pair[1])),
                           (actionnumsre, str(check.uactions[user])),
                           (randomlinere, check.randomlines[user].replace('<', '&lt;').replace('>', '&gt;')),
                              (swearnumre, str(check.numswears[user])),
                             (swearstagre, "")
                          )
            alluserstemp = allusers
            alluserstemp = subSection(alluserstemp, sublist)
            allusersstr.append(alluserstemp)
        if not check.linenums_top[detailusers:]:
            html = re.sub(allusersSre, "", html)
            html = re.sub(allusersre, "", html)
            allusersstr = ""
        elif endl == -1:
            alluserstemp = re.search(alluserslastre, html).group(1)
            user = check.linenums_top[-1][0]
            number = usertop[-1][0]
            sublist =   ((usernumberre, str(number)),
                         (usernamere, user),
                         (linenumsre, str(check.linenums[user])),
                         (actionnumsre, str(check.uactions[user])),
                         (randomlinere, check.randomlines[user].replace('<', '&lt;').replace('>', '&gt;')),
                           (swearnumre, str(check.numswears[user])),
                           (swearstagre, "")
                        )
            alluserstemp = subSection(alluserstemp, sublist)
            lasty = alluserstemp.encode('utf-8')
        allusersstr = u''.join(allusersstr).encode('utf-8')
    else:
        allusersstr = ''
    html = re.sub(allusersre, allusersstr, html)
    html = re.sub(allusersStagre, "", html)
    html = re.sub(alluserslastre, lasty, html)

    cws = []
    cwshelp = []
    
    oddmod, evenmod = (1, 0) if (topwords % 2 == 0) else (0, 1)

    if re.search(cwre, html):
        cws.append((re.search(cwre, html).group(1), [0, topwords, 1], cwre))
    if re.search(cwoddre, html):
        cws.append((re.search(cwoddre, html).group(1), [0, topwords - oddmod, 2], cwoddre))
    if re.search(cwevenre, html):
        cws.append((re.search(cwevenre, html).group(1), [1, topwords - evenmod, 2], cwevenre))
    if re.search(cwlastre, html):
        cws.append((re.search(cwlastre, html).group(1), [-1, 0], cwlastre))
        cwshelp.append([0, topwords, 1])
    if re.search(cwoddlastre, html):
        cws.append((re.search(cwoddlastre, html).group(1), [-1, 1], cwoddlastre))
        cwshelp.append([0, topwords - oddmod, 2])
    if re.search(cwevenlastre, html):
        cws.append((re.search(cwevenlastre, html).group(1), [-1, 0], cwevenlastre))
        cwshelp.append([1, topwords - evenmod, 2])
    if cws:
        wordtop = list(enumerate(check.wordlist))
        for commonwords, sss, tags in cws:
            commonwordsstr = []
            if sss in cwshelp:
                sss[1] = len(check.wordlist[:sss[1]]) - 1
            if len(sss) == 2:
                allthewords = wordtop[:topwords - sss[1]][sss[0]:]
            else:
                allthewords = wordtop[:topwords][sss[0]:sss[1]:sss[2]]
            for number, pair in allthewords:
                word = pair[0]
                sublist =     ((wordre, str(word)),
                               (usesre, str(pair[1])),
                               (numberre, str(number + 1))
                              )
                commonwordstemp = commonwords
                commonwordstemp = subSection(commonwordstemp, sublist)
                commonwordsstr.append(commonwordstemp)
            commonwordsstr = u''.join(commonwordsstr).encode('utf-8')
            html = re.sub(tags, commonwordsstr, html)
    return html

def outputLogHTML(check, starttime):
    with open(os.path.join(pycspath, 'resources', 'themes', template, 'index.html'), 'r') as infile:
        html = infile.read()

    html = generateHTML(html, check, starttime)

    resourcecomparison = dircmp(os.path.join(pycspath, 'resources', 'themes', template), os.path.join(pycspath, 'output'))
    if resourcecomparison.left_only or resourcecomparison.right_only:
        distutils.dir_util.remove_tree(os.path.join(pycspath, 'output'))
        distutils.dir_util.copy_tree(os.path.join(pycspath, 'resources', 'themes', template), os.path.join(pycspath, 'output'))
    superfile = open(os.path.join(pycspath, 'output', 'index.html'), 'w')
    superfile.write(html)
    superfile.close()
if __name__ == '__main__':
    x = time.time()
    outputLogHTML(Logs(pycspath, ["testlog.log"], printprogress), x)
