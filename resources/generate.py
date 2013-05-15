# -*- coding: cp1252 -*-

import sys      ## Needed for importing remote modules
import os       ## Needed for creating directories and loading logs.

## sys.path.insert(0, os.getcwd() + r'\resources')

import startops  ## Initializing program with variables and such

## -- The next few lines sets startops variables -- ##

swears          =   startops.swears         ## Options
aliases         =   startops.aliases        ##
ignore          =   startops.ignore         ##
minlength       =   startops.minlength      ##
ignored_words   =   startops.ignored_words  ##
logformat       =   startops.logformat      ##
pathoverride    =   startops.pathoverride   ##
logdirs         =   startops.logdirs        ##
lognames        =   startops.lognames       ##
printprogress   =   startops.printprogress  ##

pattern_username    =   startops.pattern_username       ## Regexes for line matching
pattern_useraction  =   startops.pattern_useraction     ##
pattern_saidwords   =   startops.pattern_saidwords      ##
pattern_actionwords =   startops.pattern_actionwords    ##
pattern_time        =   startops.pattern_time           ##

hnum            =   startops.hnum   ## Time format help
mnum            =   startops.mnum   ##

## ------------------------------------------------ ##

import re       ## Needed for matching count objects.
import confutil ## Needed for saving configs and such.
import random   ## Needed for randomly chosen lines, etc.


def nofunc(*args): ## Here as a placeholder function
    """Does absolutely nothing."""
    pass

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
    try:
        linenums[poster] += 1 ## Poster already exists in linenums
    except KeyError:
        if check:
            comparison = compareAndAlias(poster, linenums) ## Checks for aliases
            if comparison:
                try:
                    linenums[comparison] += 1 ## Comparison exists
                except KeyError:
                    linenums[comparison] =  1 ## Comparison does not exist
            else:
                linenums[poster] = 1 ## Poster has no alias and is new to linenums    return linenums
        else:
            linenums[poster] = 1

class Logs(object):
    """Handles IRC logs, and the generation of Python-friendly statistics based on them."""
    def __init__(self, directory, logs, printprogress=False):
        self.directory = directory
        self.logs = logs
        if type(logs) == list: ## Adds some freedom/error handling to the config
            self.paths = [directory + log for log in self.logs]
        else:
            self.paths = [directory + log]
        self.printprogress = printprogress
        self.genEverything()

    ## --- Dummy variable section
    
    linenums    = {}
    uactions    = {}
    actionsonly = {}
    userlines   = {}
    randomlines = {}
    wordnums    = {}
    swears      = {}
    times       = {
                     0: 0,  1: 0,  2: 0,  3: 0,  4: 0,  5: 0,
                     6: 0,  7: 0,  8: 0,  9: 0, 10: 0, 11: 0,
                    12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0,
                    18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0
                  }
    wordlist = [[None, 0]]
    totallines = 0

    ## ---

    find_username       =   re.compile(pattern_username     ) ## Regex patterns
    find_useraction     =   re.compile(pattern_useraction   ) ##
    find_saidwords      =   re.compile(pattern_saidwords    ) ##
    find_actionwords    =   re.compile(pattern_actionwords  ) ##
    find_time           =   re.compile(pattern_time         ) ##

    def countLines(self, special=nofunc):
        """Generates stats for number of lines per user, and executes 'special' while it's at it."""
        for log in self.paths: ## Counts things in every supplied log
            infile = open(log, 'r')
            for line in infile:
                
                self.totallines += 1 ## Counts every line in the log. Might want to effectivize this somehow

                ## -Creates search objects based on earlier patterns- ##
                un          =   re.search(self.find_username, line      ) ## Username
                ua          =   re.search(self.find_useraction, line    ) ## Username in actions
                unw         =   re.search(self.find_saidwords, line     ) ## Said words
                uaw         =   re.search(self.find_actionwords, line   ) ## Action words
                linetime    =   re.search(self.find_time, line          ) ## Time of line
                ## -------------------------------------------------- ##
                
                if linetime:
                    linetime    =   (
                                        linetime.group(hnum), ## Allows for different time formats
                                        linetime.group(mnum), ##
                                    )
                
                if un and un.group(1).lower().strip() not in [x.lower() for x in ignore]:
                    ## Only does anything at all if there's a valid, non-ignored username
                    u = compareAndAlias(un.group(1), self.linenums)
                    if not u: ## For users without alias
                        u = un.group(1)
                    special(u, unw.group(1), '', linetime) ## Executes special functions
                    ## Special argument format:
                    ## Username, line, prefix, time of line
                    self.linenums = addUn(un.group(1), self.linenums)
                elif ua and ua.group(1).lower().strip() not in [x.lower() for x in ignore]:
                    ## Only does anything at all if there's a valid, non-ignored username
                    u = compareAndAlias(ua.group(1), self.linenums)
                    if not u: ## For users without alias
                        u = ua.group(1)
                    special(u, uaw.group(1), ua.group(1) + ' ', linetime) ## Executes special functions
                    ## Special argument format:
                    ## Username, line, prefix, time of line
                    self.uactions = addUn(ua.group(1), self.uactions)
            uactions_org = self.uactions.copy() ## Creates iterable dictionary, original will be modified

            for comparison in uactions_org: ## Adds user action lines to total line numbers for said user
                c = compareAndAlias(comparison, self.linenums)
                if c:
                    self.linenums[c] += self.uactions[comparison]
                else: ## Makes sure no ChanServs or such make it into the stats
                    self.actionsonly[comparison] = self.uactions.pop(comparison, {'NotWorking': 1})

    def listLines(self, username, line, t): ## Could theoretically merge this with addUn
        """Assigns every user a list of every line they've said."""
        line = line.strip() ## No newlines or unnecessary whitespace
        try:
            self.userlines[username].append(t + line)
            return
        except KeyError:
            c = compareAndAlias(username, self.linenums)
            if c:
                try:
                    self.userlines[c].append(t +line)
                except KeyError:
                    self.userlines[c] = [t + line]
            else:
                self.userlines[username] = [t + line]

    def fixListLines(self): ## Prevents ChanServ-like bots from getting into the statistics
        """Makes sure action-only users don't get line lists."""
        userlines_org = self.userlines.copy()
        for l in userlines_org:
            if l not in self.linenums:
                del self.userlines[l]
                
    def countWords(self, username, words, t):
        """Counts words and assigns number to user."""
        for w in words:
            if len(w) >= minlength and\
            w.lower() not in [word.lower() for word in ignored_words] and\
            username.lower() not in [un.lower() for un in ignore] and\
            not t:
                try:
                    self.wordnums[w.lower()] += 1
                except KeyError:
                    self.wordnums[w.lower()] = 1

    def countSwears(self, username, words):
        """Counts swears and assigns number to user."""
        for w in words:
            for s in swears:
                bob = re.compile("^" + s + "$", re.IGNORECASE)  ## Master of variable names
                if re.search(bob, w.lower()):
                    try:
                        self.swears[username][w.lower()] += 1
                    except KeyError: ## Standard key creation
                        try:
                            self.swears[username][w.lower()] = 1
                        except KeyError:
                            self.swears[username] = {w.lower(): 1}

    def commonWords(self):
        """Counts how many times every word was used"""
        for w in self.wordnums:
            for number, pair in enumerate(self.wordlist):
                if self.wordnums[w] >= pair[1]:
                    self.wordlist.insert(number, [w, self.wordnums[w]])
                    break
            else:
                self.wordlist.append([w, self.wordnums[w]])
        del self.wordlist[-1]

    def timeCount(self, time):
        """Adds 1 to the time dictionary for every line that was posted during that hour."""
        self.times[int(time[0])] += 1

    def returnWords(self, username, line):
        """Gets a list of the words used in 'line'."""
        if line[:len(username)].lower() != username.lower(): ## Doesn't count actions' first words - the usernames
            return re.split("[;:\(\)@\.\s\!\?\",]+", line)              ## Splits at any non-letter
        return re.split("[;:\(\)@\.\s\!\?\",]+", line[len(username):])  ## ... or mid-word delimiter

    def specialFuncs(self, username, line, prefix, time):
        """Does a multitude of special functions."""
        words = self.returnWords(username, line)
        self.countWords(username, words, prefix)
        self.countSwears(username, words)
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
                print "Cleaning up line list..."
            self.fixListLines()
            if self.printprogress:
                print "Choosing random lines..."
            self.randLines()
            if self.printprogress:
                print "Organizing words..."
            self.commonWords()
            if self.printprogress:
                print "Done!"
        else:
            print "No logs."
