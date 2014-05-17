# -*- coding: UTF-8 -*-

import sys      ## Needed for importing remote modules
import os       ## Needed for creating directories and loading logs.
import re       ## Needed for matching count objects.
import startops ## Initializing program with variables and such
from collections import Counter, defaultdict

## -- The next few lines sets startops variables -- ##

swears          =   startops.swears         ## Options
aliases         =   startops.aliases        ##
ignore          =   startops.ignore         ##
minlength       =   startops.minlength      ##
ignored_words   =   startops.ignored_words  ##
logformat       =   startops.logformat      ##
pathoverride    =   startops.pathoverride   ##
lognames        =   startops.lognames       ##
printprogress   =   startops.printprogress  ##
channelname     =   startops.channelname    ##
pycspath        =   startops.pycspath       ##
detailusers     =   startops.detailusers    ##
topwords        =   startops.topwords       ##
template        =   startops.template       ##
allusersbool    =   startops.allusersbool   ##
allusersnum     =   startops.allusersnum    ##

pattern_said_line   =   startops.pattern_said_line      ## Regexes for line matching
pattern_action_line =   startops.pattern_action_line    ##
pattern_time        =   startops.pattern_time           ##

if not [x for x in swears if x not in ('swear1', 'swear2')]:
    print swears
    swearcount = False
else:
    swearcount = True
    swearsre = re.compile('|'.join(swears), re.IGNORECASE | re.UNICODE)

## ------------------------------------------------ ##

import confutil ## Needed for saving configs and such.
import random   ## Needed for randomly chosen lines, etc.


def compareNames(poster, linenums):
    """Matches usernames regardless of case."""
    if poster in linenums:
        return poster
    for comparison in linenums: ## Checks in existing name dictionary
        if poster.lower() == comparison.lower():
            return comparison
    return False

def hasAlias(name, adict=aliases):
    """Compares 'name' to names in adict."""
    for comparison in adict: ## Checks in existing aliases dictionary
        if name.lower() in [a.lower() for a in adict[comparison]]:
            return comparison
    return False

def compareAndAlias(poster, linenums):
    """Shorthand function for both compareNames and hasAlias."""
    comparison = compareNames(poster, linenums)
    if comparison: ## Using compareNames
        return comparison
    comparison = hasAlias(poster)
    if comparison: ## Using hasAlias
        return comparison
    return False

def addUn(poster, linenums, check=False):
    """Returns 'linenums' with the appropriate key for 'poster' updated."""
    if not check:
        linenums[poster] += 1
    else:
        poster = compareAndAlias(poster, linenums) or poster
        linenums[poster] += 1
    return linenums


class Logs(object):
    """Handles IRC logs, and the generation of Python-friendly statistics based on them."""
    def __init__(self, directory, logs, printprogress=False):
        self.directory = directory
        self.logs = logs
        if type(logs) == list: ## Adds some freedom/error handling to the config
            self.paths = [os.path.join(directory, log) for log in self.logs]
        else:
            self.paths = [os.path.join(directory, logs)]
        self.printprogress = printprogress
        self.genEverything()

    ## --- Dummy variable section
    
    linenums    = Counter()
    uactions    = Counter()
    actionsonly = {}
    userlines   = defaultdict(list)
    randomlines = {}
    wordnums    = Counter()
    swears      = {}
    numswears   = Counter()
    times       = {hour: 0 for hour in range(24)}
    times_ordered = []
    wordlist    = [[None, 0]]
    linenums_top= [[None, 0]]
    uactions_top= [[None, 0]]
    totallines  = 0

    ## ---

    find_said_line      =   re.compile(pattern_said_line    ) ## Regex patterns
    find_action_line    =   re.compile(pattern_action_line  ) ##
    find_time           =   re.compile(pattern_time         ) ##

    def countLines(self, special=lambda *args: None):
        """Generates stats for number of lines per user, and executes 'special' while it's at it."""
        for log in self.paths: ## Counts things in every supplied log
            infile = open(log, 'r')
            linelist = [unicode(line, 'utf-8') for line in infile]
            for line in linelist:            

                ## -Creates search objects based on earlier patterns- ##
                un          =   re.search(self.find_said_line, line     ) ## /say lines
                ua          =   re.search(self.find_action_line, line   ) ## /me lines
                linetime    =   re.search(self.find_time, line          ) ## Time of line
                ## -------------------------------------------------- ##

                if un or ua or linetime:
                    self.totallines += 1 ## Counts every line in the log.
                
                if linetime:
                    linetime    =   (
                                        linetime.group('hour'   ), ## Allows for different time formats
                                        linetime.group('minute' ), ##
                                    )
                
                if un and un.group('nickname').lower().strip() not in [x.lower() for x in ignore]:
                    ## Only does anything at all if there's a valid, non-ignored username
                    u = compareAndAlias(un.group('nickname'), self.linenums)
                    if not u: ## For users without alias
                        u = un.group('nickname')
                    special(u, un.group('words'), '', linetime) ## Executes special functions
                    ## Special argument format:
                    ## Username, line, prefix, time of line
                    self.linenums = addUn(u, self.linenums)
                elif ua and ua.group('nickname').lower().strip() not in [x.lower() for x in ignore]:
                    ## Only does anything at all if there's a valid, non-ignored username
                    u = compareAndAlias(ua.group('nickname'), self.linenums)
                    if not u: ## For users without alias
                        u = ua.group('nickname')
                    special(u, ua.group('words'), ua.group('nickname') + ' ', linetime) ## Executes special functions
                    ## Special argument format:
                    ## Username, line, prefix, time of line
                    self.uactions = addUn(u, self.uactions)

            infile.close() ## I can't believe it took me this long to add this
            
            uactions_org = self.uactions.copy() ## Creates iterable dictionary, original will be modified

            for comparison in uactions_org: ## Adds user action lines to total line numbers for said user
                c = compareAndAlias(comparison, self.linenums)
                if c:
                    self.linenums[c] += self.uactions[comparison]
                else: ## Makes sure no ChanServs or such make it into the stats
                    self.actionsonly[comparison] = self.uactions.pop(comparison, {'NotWorking': 1})

    def __repr__(self): ## Mostly useful for testing
        return "Logs: " + str(self.paths) +                                 \
        '\nTotal number of lines: ' + str(self.totallines) +                \
        '\nTotal number of actions: ' + str(sum(self.uactions.values())) +  \
        '\nTotal number of swears: ' + str(sum(self.numswears.values()))

    def listLines(self, username, line, t): ## Could theoretically merge this with addUn
        """Assigns every user a list of every line they've said."""
        line = line.strip() ## No newlines or unnecessary whitespace
        username = compareAndAlias(username, self.linenums) or username
        self.userlines[username].append(t + line)

    def fixListLines(self): ## Prevents ChanServ-like bots from getting into the statistics
        """Makes sure action-only users don't get line lists."""
        userlines_org = self.userlines.copy()
        for l in userlines_org:
            if l not in self.linenums:
                del self.userlines[l]
                
    def countWords(self, username, words, t):
        """Counts words.""" ## ...That was a very in-depth description.
        for w in words:
            if len(w) >= minlength and\
            w.lower() not in [word.lower() for word in ignored_words] and\
            username.lower() not in [un.lower() for un in ignore] and\
            not t:
                self.wordnums[w.lower()] += 1

    def topUsers(self, linenums=linenums):
        """Sorts linenums by number of lines per user."""
        return sorted(linenums.iteritems(), key=lambda pair: pair[1], reverse=True)

    def countSwears(self, username, line):
        """Counts swears and assigns number to user."""
        self.numswears[username] += len(re.findall(swearsre, line))

    def fillNonfull(self, nonfull):
        for user in [u for u in self.linenums if u not in nonfull]:
            nonfull[user] = 0
        return nonfull

    def commonWords(self):
        """Sorts words into self.wordlist by number of times used."""
        self.wordlist = sorted(self.wordnums.iteritems(), key=lambda pair: pair[1], reverse=True)

    def timeCount(self, time):
        """Adds 1 to the time dictionary for every line that was posted during that hour."""
        self.times[int(time[0])] += 1

    def returnWords(self, username, line):
        """Gets a list of the words used in 'line'."""
        return re.split(u"[\\;:\(\)@\.\s\!\?\",/*=><~]+", line)             ## Splits at any non-letter/number or mid-word delimiter

    def specialFuncs(self, username, line, prefix, time):
        """Does a multitude of special functions."""
        words = self.returnWords(username, line)
        self.countWords(username, words, prefix)
        self.countSwears(username, line)
        self.listLines(username, line, prefix)
        self.timeCount(time)
    
    def randLines(self):
        """Chooses a random line for each user."""
        for user in self.userlines:
            randtemp = random.choice(self.userlines[user])
            self.randomlines[user] = randtemp

    def genEverything(self):
        """Generates all stats. Used in __init__."""
        if self.logs:
            if self.printprogress:
                print "Scanning lines..."
            self.countLines(self.specialFuncs)
            if self.printprogress:
                print "Cleaning up..."
            self.fixListLines()
            if swearcount:
                self.numswears = self.fillNonfull(self.numswears)
            self.uactions = self.fillNonfull(self.uactions)
            if self.printprogress:
                print "Choosing random lines..."
            self.randLines()
            if self.printprogress:
                print "Sorting words..."
            self.commonWords()
            if self.printprogress:
                print "Sorting users..."
            self.linenums_top = self.topUsers()
            self.uactions_top = self.topUsers(self.uactions)
            self.times_ordered = sorted(self.times.iteritems())
            if self.printprogress:
                print "Statistics generation complete!"
        else:
            print "No logs."
