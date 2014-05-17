# -*- coding: UTF-8 -*-

import os                   ## Needed for file copying, intelligent paths
from generate import *      ## Needed for... well, generating stats
import time                 ## Needed for timing the stat generation while testing
import distutils.core       ## Needed for directory copying
from filecmp import dircmp  ## Needed for directory comparison
import re                   ## Needed for matching/replacing tags
import random               ## Needed for choosing random lines

## Regular expressions for tags ##

usernumberre    = re.compile("%usernumber%" )
usernamere      = re.compile("%username%"   )
linenumsre      = re.compile("%linenums%"   )
actionnumsre    = re.compile("%actionnums%" )
randomlinere    = re.compile("%randomline%" )
newrandomlinere = re.compile("%newrandom%"  )

channelnamere   = re.compile("%channelname%")
gentimere       = re.compile("%gentime%"    )

dawnpre         = re.compile("%dawnpercent%"        )
morningpre      = re.compile("%morningpercent%"     )
daypre          = re.compile("%daypercent%"         )
nightpre        = re.compile("%nightpercent%"       )

dawnpnumre      = re.compile("%dawnpercent-([0-9]+)%"     )
morningpnumre   = re.compile("%morningpercent-([0-9]+)%"  )
daypnumre       = re.compile("%daypercent-([0-9]+)%"      )
nightpnumre     = re.compile("%nightpercent-([0-9]+)%"    )

timere          = re.compile("%timefraction-(?P<starttime>[0-9]{1,2})-(?P<endtime>[0-9]{1,2})-(?P<fractionof>[0-9]+)%")

totallinesre    = re.compile("%totallines%" )
swearnumre      = re.compile("%swears%"     )

userstatsre     = re.compile("(?:<!--\s*)?\[userstats\](?:\s*-->)?(.*?)(?:<!--\s*)?\[/userstats\](?:\s*-->)?", re.DOTALL               )
userstatslastre = re.compile("(?:<!--\s*)?\[userstats-last\](?:\s*-->)?(.*?)(?:<!--\s*)?\[/userstats-last\](?:\s*-->)?", re.DOTALL     )
swearsre        = re.compile("(?:<!--\s*)?\[swears\].*\[/swears\](?:\s*-->)?", re.DOTALL                       )
allusersre      = re.compile("(?:<!--\s*)?\[allusers\](?:\s*-->)?(.*?)(?:<!--\s*)?\[/allusers\](?:\s*-->)?", re.DOTALL                 )
allusersSre     = re.compile("(?:<!--\s*)?\[allusers-section\](?:\s*-->)?(.*?)(?:<!--\s*)?\[/allusers-section\](?:\s*-->)?", re.DOTALL )
alluserslastre  = re.compile("(?:<!--\s*)?\[allusers-last\](?:\s*-->)?(.*?)(?:<!--\s*)?\[/allusers-last\](?:\s*-->)?", re.DOTALL       )
alluserslasttagre = re.compile("(?:<!--\s*)?\[/?allusers-last\](?:\s*-->)?"                                    )
allusersStagre  = re.compile("(?:<!--\s*)?\[/?allusers-section\](?:\s*-->)?"                                   )
swearstagre     = re.compile("(?:<!--\s*)?\[/?swears\](?:\s*-->)?"                                             )

cwre            = re.compile("(?:<!--\s*)?\[commonwords\](?:\s*-->)?(.*?)(?:<!--\s*)?\[/commonwords\](?:\s*-->)?", re.DOTALL           )
cwoddre         = re.compile("(?:<!--\s*)?\[commonwords-odd\](?:\s*-->)?(.*?)(?:<!--\s*)?\[/commonwords-odd\](?:\s*-->)?", re.DOTALL   )
cwevenre        = re.compile("(?:<!--\s*)?\[commonwords-even\](?:\s*-->)?(.*?)(?:<!--\s*)?\[/commonwords-even\](?:\s*-->)?", re.DOTALL )

cwlastre        = re.compile("(?:<!--\s*)?\[commonwords-last\](?:\s*-->)?(.*?)(?:<!--\s*)?\[/commonwords-last\](?:\s*-->)?", re.DOTALL )
cwoddlastre     = re.compile("(?:<!--\s*)?\[commonwords-odd-last\](?:\s*-->)?(.*?)(?:<!--\s*)?\[/commonwords-odd-last\](?:\s*-->)?", re.DOTALL     )
cwevenlastre    = re.compile("(?:<!--\s*)?\[commonwords-even-last\](?:\s*-->)?(.*?)(?:<!--\s*)?\[/commonwords-even-last\](?:\s*-->)?", re.DOTALL   )

wordre          = re.compile("%word%"       )
usesre          = re.compile("%uses%"       )
numberre        = re.compile("%number%"     )

##

def timePercents(check):
    """Returns a tuple of the percentages of lines posted between 0 and 6, 6 and 12, 12 and 18, and 18 and 0, respectively."""
    totaltimelines = float(sum(check.times.values()))
    time1 = (sum((x[1] for x in check.times_ordered[:6])) / totaltimelines) * 100
    time2 = (sum((x[1] for x in check.times_ordered[6:12])) / totaltimelines) * 100
    time3 = (sum((x[1] for x in check.times_ordered[12:18])) / totaltimelines) * 100
    time4 = (sum((x[1] for x in check.times_ordered[18:])) / totaltimelines) * 100
    return round(time1, 1), round(time2, 1), round(time3, 1), round(time4, 1) ## Rounds to one decimal

def subSeveral(s, t):
    """Returns string 's' with all items in list 't' being re.sub'd - first element is pattern, second is replacement."""
    for pattern, replacement in t:
        s = re.sub(pattern, replacement, s)
    return s

def generateHTML(html, check, starttime, endtime=None):
    """Generates a HTML page based on a template, a Logs object and a start time."""
    y = time.time() if not (endtime) else endtime ## Sets finish time. Is it cheating to do this before generating the actual page...?

    time1, time2, time3, time4 = timePercents(check)
    dawnpercent, morningpercent, daypercent, nightpercent = [str(x) for x in (time1, time2, time3, time4)] ## String versions with slightly more reader-friendly names
    
    totaltimelines = float(sum(check.times.values()))
    
    ## Replaces "global" tags ##
    
    html = re.sub(channelnamere     , channelname.encode('utf-8')   , html)
    html = re.sub(gentimere         , str(round(y - starttime, 2)), html)

    html = re.sub(dawnpre           , dawnpercent   , html)
    html = re.sub(morningpre        , morningpercent, html)
    html = re.sub(daypre            , daypercent    , html)
    html = re.sub(nightpre          , nightpercent  , html)

    ## These functions take number from template, multiplies percentages to get fractions of whatever number template supplied.
    dawnf       = lambda x: str(round(time1 * (float(x.group(1)) / 100), 1)) ##
    morningf    = lambda x: str(round(time2 * (float(x.group(1)) / 100), 1)) ##
    dayf        = lambda x: str(round(time3 * (float(x.group(1)) / 100), 1)) ##
    nightf      = lambda x: str(round(time4 * (float(x.group(1)) / 100), 1)) ##

    ## Using previous functions, replaces everything with correct fractions
    html = re.sub(dawnpnumre    , dawnf    , html)
    html = re.sub(morningpnumre , morningf , html)
    html = re.sub(daypnumre     , dayf     , html)
    html = re.sub(nightpnumre   , nightf   , html)
    ##
    
    def timeFractions(tag):
        offset = 24 if (int(tag.group('endtime')) <= int(tag.group('starttime'))) else 0
        return str(round((sum([x[1] for x in (check.times_ordered * 2)[int(tag.group('starttime')):int(tag.group('endtime')) + offset]]) / totaltimelines) * int(tag.group('fractionof')), 1))

    html = re.sub(timere        , timeFractions, html)
    
    html = re.sub(totallinesre, str(check.totallines), html)

    ##

    usertop = list(enumerate(check.linenums_top)) ## Allows for static enumeration
    ## Don't want the enumeration to start from 0 in every list slice.

    if not swearcount: ## Removes swear tags if swear count is off
        html = re.sub(swearsre, "", html)
        html = re.sub(swearre, "", html)

    if re.search(userstatsre, html): ## Top users
        endl = -1 if (re.search(userstatslastre, html)) else detailusers ## Sets end index for usertop
        userstats = re.search(userstatsre, html).group(1) ## Sets HTML to be repeated for each user
        userstatsstr = [] ## Dummy list
        for number, pair in usertop[:detailusers][:endl]: ## Double slice for endl to work
            user = pair[0]

            sublist = ((usernumberre, str(number)),
                       (usernamere, user),
                       (linenumsre, str(pair[1])),
                       (actionnumsre, str(check.uactions[user])),
                       (randomlinere, check.randomlines[user].replace('<', '&lt;').replace('>', '&gt;')),
                       (newrandomlinere, lambda x: random.choice(check.userlines[user]).replace('<', '&lt;').replace('>', '&gt;')),
                       (swearnumre, str(check.numswears[user])),
                       (swearstagre, "")
                       )
            userstatstemp = userstats
            userstatstemp = subSeveral(userstatstemp, sublist) ## Creates version of userstats with stats substituted in
            userstatsstr.append(userstatstemp) ## Will be joined later

        if endl == -1: ## If [userstats-last] is present
            ## Same thing as previous part, except only once
            userstatslast = re.search(userstatslastre, html).group(1)
            user, number = usertop[:detailusers][endl][1][0], usertop[:detailusers][endl][0]
            sublist = ((usernumberre, str(number)),
                       (usernamere, user),
                       (linenumsre, str(pair[1])),
                       (actionnumsre, str(check.uactions[user])),
                       (randomlinere, check.randomlines[user].replace('<', '&lt;').replace('>', '&gt;')),
                       (newrandomlinere, lambda x: random.choice(check.userlines[user]).replace('<', '&lt;').replace('>', '&gt;')),
                       (swearnumre, str(check.numswears[user])),
                       (swearstagre, "")
                       )
            userstatstemp = userstatslast
            userstatstemp = subSeveral(userstatstemp, sublist)
            html = re.sub(userstatslastre, userstatstemp.encode('utf-8'), html)         
        userstatsstr = u''.join(userstatsstr).encode('utf-8')
    else:
        userstatsstr = ''
        html = re.sub(userstatslastre, "", html)
    html = re.sub(userstatsre, userstatsstr, html)
    
    alluserstotal = len(check.linenums_top) if not (allusersnum) else allusersnum
    lasty = "" ## Needed dummy variable
    
    if allusersbool and re.search(allusersre, html) and check.linenums_top[detailusers:alluserstotal]: ## Same thing as previous block, except different tags
        endl = 1 if (re.search(alluserslasttagre, html)) else 0
        allusersstr = []
        allusers = re.search(allusersre, html).group(1)
        for number, pair in usertop[detailusers:alluserstotal - endl]:
            user = pair[0]
            sublist =     ((usernumberre, str(number)),
                           (usernamere, user),
                           (linenumsre, str(pair[1])),
                           (actionnumsre, str(check.uactions[user])),
                           (randomlinere, check.randomlines[user].replace('<', '&lt;').replace('>', '&gt;')),
                           (newrandomlinere, lambda x: random.choice(check.userlines[user]).replace('<', '&lt;').replace('>', '&gt;')),
                           (swearnumre, str(check.numswears[user])),
                           (swearstagre, "")
                          )
            alluserstemp = allusers
            alluserstemp = subSeveral(alluserstemp, sublist)
            allusersstr.append(alluserstemp)
        if endl == 1:
            alluserstemp = re.search(alluserslastre, html).group(1)
            user = check.linenums_top[alluserstotal - endl][0]
            number = usertop[-1][0]
            sublist =   ((usernumberre, str(number)),
                         (usernamere, user),
                         (linenumsre, str(check.linenums[user])),
                         (actionnumsre, str(check.uactions[user])),
                         (randomlinere, check.randomlines[user].replace('<', '&lt;').replace('>', '&gt;')),
                         (newrandomlinere, lambda x: random.choice(check.userlines[user]).replace('<', '&lt;').replace('>', '&gt;')),
                         (swearnumre, str(check.numswears[user])),
                         (swearstagre, "")
                        )
            alluserstemp = subSeveral(alluserstemp, sublist)
            lasty = alluserstemp.encode('utf-8')
        allusersstr = u''.join(allusersstr).encode('utf-8')
    else:
        allusersstr = ''
        html = re.sub(allusersSre, "", html)
    html = re.sub(allusersre, allusersstr, html)
    html = re.sub(allusersStagre, "", html)
    html = re.sub(alluserslastre, lasty, html)

    cws = []
    cwshelp = []

    ## I wrote this code when I was very tired.    
    oddmod, evenmod = (1, 0) if (topwords % 2 == 0) else (0, 1)
    ## ...What do I know, it works.
    
    ## Okay, after much thinking. HERE'S HOW/WHY IT WORKS.
    ## oddmod and evenmod are subtracted from the "stop" index in the next part.
    ## Note that cwoddre and cwevenre are substituted with even and odd indices of the top words list, respectively. This makes things a bit confusing.
    ## If a "last" tag is present, we want to make sure that the last entry isn't included in the substitute for the normal tag.
    ## This means that we have to subtract one entry at the end.
    ## The below code subtracts 1 from the stop index if a "last" tag is present.
    ## 1 will only do it, however, if the stop index is 1 over the last entry.
    ## If the number is, for example, 37, one will be subtracted in order to get 36.
    ## This will exclude index 36 (and subsequently 35 if a last tag is present), which is fine for the odd entries (which are the cwevenre ones).
    ## However, we need to remove index 34 too for the even entries (which are the cwoddre ones).
    ## Since 1 is always subtracted, we need to subtract 1 extra. This is what oddmod and evenmod do.
    ## These modifiers are also used to fetch the correct last entry.
    ## This is reversed if topwords is even.
    ## The previous variables do this by modifying the stop indices by either -1 or 0!

    ## Checking for different common words tags
    
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
        cws.append((re.search(cwoddlastre, html).group(1), [-1, oddmod], cwoddlastre))
        cwshelp.append([0, topwords - oddmod, 2])
    if re.search(cwevenlastre, html):
        cws.append((re.search(cwevenlastre, html).group(1), [-1, evenmod], cwevenlastre))
        cwshelp.append([1, topwords - evenmod, 2])

    ## The "last" tag checks append the same start, stop, step as the corresponding section tags to a help list.
    ## This allows the next block to keep the last entry out of the main sections, if a "last" tag is present.

    ##

    if cws:
        wordtop = list(enumerate(check.wordlist))
        for commonwords, sss, tags in cws:
            commonwordsstr = []
            if sss in cwshelp: ## Subtracts 1 from stop index if a "last" tag is present
                sss[1] = len(check.wordlist[:sss[1]]) - 1
            if len(sss) == 2: ## List of words contains only last entry if one of the last REs are being used
                allthewords = wordtop[:topwords - sss[1]][sss[0]:]
            else: ## Creates a list of words to be substituted in
                allthewords = wordtop[:topwords][sss[0]:sss[1]:sss[2]]
            for number, pair in allthewords:
                word = pair[0]
                sublist =     ((wordre, unicode(word)),
                               (usesre, str(pair[1])),
                               (numberre, str(number + 1))
                              )
                commonwordstemp = commonwords
                commonwordstemp = subSeveral(commonwordstemp, sublist)
                commonwordsstr.append(commonwordstemp)
            commonwordsstr = u''.join(commonwordsstr).encode('utf-8')
            html = re.sub(tags, commonwordsstr, html)
    return html ## Returns the page with everything substituted in

def outputLogHTML(check, starttime):
    """Outputs a HTML file (using generateHTML()) based on a Logs object and a start time. Copies/deletes files from output directory as necessary. Not very dynamic at all."""
    with open(os.path.join(pycspath, 'resources', 'themes', template, 'index.html'), 'r') as infile:
        html = infile.read()

    if printprogress:
        print "Generating page..."
        
    html = generateHTML(html, check, starttime)

    resourcecomparison = dircmp(os.path.join(pycspath, 'resources', 'themes', template), os.path.join(pycspath, 'output'))
    if resourcecomparison.left_only or resourcecomparison.right_only or [x for x in resourcecomparison.diff_files if x not in ('index.html', '.DS_Store')]:
        ## Copies theme resources if not already in output directory

        if printprogress:
            print "Copying theme files..."

        distutils.dir_util.remove_tree(os.path.join(pycspath, 'output'))
        distutils.dir_util.copy_tree(os.path.join(pycspath, 'resources', 'themes', template), os.path.join(pycspath, 'output'))
    with open(os.path.join(pycspath, 'output', 'index.html'), 'w') as superfile:
        superfile.write(html)

    if printprogress:
        print "Done!"
    
if __name__ == '__main__':
    ## Testing code!
    x = time.time()
    outputLogHTML(Logs(pycspath, ["testlog.log"], printprogress), x)
