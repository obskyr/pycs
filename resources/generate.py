# -*- coding: cp1252 -*-

import sys      ## Needed for importing remote modules
import os       ## Needed for creating directories and loading logs.

## sys.path.insert(0, os.getcwd() + r'\resources')

import startops  ## Initializing program with variables and such

## -- The next few lines sets startops variables -- ##

swears          =   startops.swears
aliases         =   startops.aliases
ignore          =   startops.ignore
minlength       =   startops.minlength
ignored_words   =   startops.ignored_words
logformat       =   startops.logformat
pathoverride    =   startops.pathoverride
logdirs         =   startops.logdirs
lognames        =   startops.lognames
printprogress   =   startops.printprogress

pattern_username    =   startops.pattern_username
pattern_useraction  =   startops.pattern_useraction
pattern_saidwords   =   startops.pattern_saidwords
pattern_actionwords =   startops.pattern_actionwords
pattern_time        =   startops.pattern_time

hnum            =   startops.hnum
mnum            =   startops.mnum
snum            =   startops.snum

## ------------------------------------------------ ##

import re       ## Needed for matching count objects.
import confutil ## Needed for saving configs and such.
import random   ## Needed for randomly chosen lines, etc.


def nofunc(*args): ## Here as a placeholder function
    """Does absolutely nothing."""
    pass

def compareNames(poster, linenums):
    for comparison in linenums:
        if poster.lower() == comparison.lower():
            return comparison
    return False

def hasAlias(name, adict=aliases):
    for comparison in aliases:
        if name.lower() in [a.lower() for a in adict[comparison]]:
            return comparison
    return False

def compareAndAlias(poster, linenums):
    comparison = compareNames(poster, linenums)
    if comparison:
        return comparison
    comparison = hasAlias(poster)
    if comparison:
        return comparison
    return False

def addUn(poster, linenums):
    try:
        linenums[poster] += 1
    except KeyError:
        comparison = compareNames(poster, linenums)
        if comparison:
            linenums[comparison] += 1
        else:
            alias = hasAlias(poster)
            if alias:
                try:
                    linenums[alias] += 1
                except KeyError:
                    linenums[alias] = 1
            else:
                linenums[poster] = 1
    return linenums

class Logs(object):
    def __init__(self, directory, logs, printprogress=False):
        self.directory = directory
        self.logs = logs
        if type(logs) == list:
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

    find_username       =   re.compile(pattern_username     )
    find_useraction     =   re.compile(pattern_useraction   )
    find_saidwords      =   re.compile(pattern_saidwords    )
    find_actionwords    =   re.compile(pattern_actionwords  )
    find_time           =   re.compile(pattern_time         )

    def countLines(self, special=nofunc):
        for log in self.paths:
            infile = open(log, 'r')
            for line in infile:
                
                self.totallines += 1
                
                un          =   re.search(self.find_username, line      )
                ua          =   re.search(self.find_useraction, line    )
                unw         =   re.search(self.find_saidwords, line     )
                uaw         =   re.search(self.find_actionwords, line   )

                linetime    =   re.search(self.find_time, line          )
                if linetime:
                    linetime    =   (
                                        linetime.group(hnum),
                                        linetime.group(mnum),
                                        linetime.group(snum)
                                    )
                
                if un and un.group(1).lower().strip() not in [x.lower() for x in ignore]:
                    u = compareAndAlias(un.group(1), self.linenums)
                    if not u:
                        u = un.group(1)
                    special(u, unw.group(1), '', linetime)
                    self.linenums = addUn(un.group(1), self.linenums)
                elif ua and ua.group(1).lower().strip() not in [x.lower() for x in ignore]:
                    u = compareAndAlias(ua.group(1), self.linenums)
                    if not u:
                        u = ua.group(1)
                    special(u, uaw.group(1), ua.group(1) + ' ', linetime)
                    self.uactions = addUn(ua.group(1), self.uactions)
            uactions_org = self.uactions.copy()
            for comparison in uactions_org:
                c = compareAndAlias(comparison, self.linenums)
                if c:
                    self.linenums[c] += self.uactions[comparison]
                else:
                    self.actionsonly[comparison] = self.uactions.pop(comparison, {'NotWorking': 1})

    def listLines(self, username, line, t) :
        line = line.strip()
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

    def fixListLines(self):
        userlines_org = self.userlines.copy()
        for l in userlines_org:
            if l not in self.linenums:
                del self.userlines[l]
                
    def countWords(self, username, words, t):
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
        for w in words:
            for s in swears:
                bob = re.compile("^" + s + "$", re.IGNORECASE)
                if re.search(bob, w.lower()):
                    try:
                        self.swears[username][w.lower()] += 1
                    except KeyError:
                        try:
                            self.swears[username][w.lower()] = 1
                        except KeyError:
                            self.swears[username] = {w.lower(): 1}

    def commonWords(self):
        for w in self.wordnums:
            for number, pair in enumerate(self.wordlist):
                if self.wordnums[w] >= pair[1]:
                    self.wordlist.insert(number, [w, self.wordnums[w]])
                    break
            else:
                self.wordlist.append([w, self.wordnums[w]])
        del self.wordlist[-1]

    def timeCount(self, time):
        self.times[int(time[0])] += 1

    def returnWords(self, username, line):
        if line[:len(username)].lower() != username.lower():
            return re.split("[;:\(\)@\.\s\!\?\",]+", line)
        return re.split("[;:\(\)@\.\s\!\?\",]+", line[len(username):])

    def specialFuncs(self, username, line, prefix, time):
        words = self.returnWords(username, line)
        self.countWords(username, words, prefix)
        self.countSwears(username, words)
        self.listLines(username, line, prefix)
        self.timeCount(time)
    
    def randLines(self):
        for user in self.userlines:
            randtemp = random.choice(self.userlines[user])
            self.randomlines[user] = randtemp

    def genEverything(self):
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
