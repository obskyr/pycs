# -*- coding: cp1252 -*-

import sys      ## Needed for importing remote modules
import os       ## Needed for creating directories and loading logs.

sys.path.insert(0, os.getcwd() + r'\resources')

import startops  ## Initializing program with variables and such

## -- The next few lines sets startops variables -- ##

swears          =   startops.swears
aliases         =   startops.aliases
ignore          =   startops.ignore
minlength       =   startops.minlength
ignored_words   =   startops.ignored_words

## ------------------------------------------------ ##

import re       ## Needed for matching count objects.
import confutil ## Needed for saving configs and such.
import random   ## Needed for randomly chosen lines, etc.


def nofunc(*args):
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
    def __init__(self, directory, logs):
        self.directory = directory
        self.logs = logs
        if type(logs) == list:
            self.paths = [directory + log for log in self.logs]
        else:
            self.paths = [directory + log]
        self.genEverything()
    linenums = {}
    uactions = {}
    actionsonly = {}
    userlines = {}
    randomlines = {}
    wordnums = {}
    swears = {}
    wordlist = [[None, 0]]
    totallines = 0
    findusername = re.compile("^[a-zA-Z]+\s[0-9]+\s[0-9:]{8}\s<([A-Za-z]+)>")
    finduseraction = re.compile("^[a-zA-Z]+\s[0-9]+\s[0-9:]{8}\s\*\s+([A-Za-z]+)\s")
    findsaidwords = re.compile("^[a-zA-Z]+\s[0-9]+\s[0-9:]{8}\s<[A-Za-z]+>(.+)")
    findactionwords = re.compile("^[a-zA-Z]+\s[0-9]+\s[0-9:]{8}\s\*\s+[A-Za-z]+\s(.+)")
    def countLines(self, special=nofunc):
        for log in self.paths:
            infile = open(log, 'r')
            for line in infile:
                self.totallines += 1
                un = re.search(self.findusername, line)
                ua = re.search(self.finduseraction, line)
                unw = re.search(self.findsaidwords, line)
                uaw = re.search(self.findactionwords, line)
                if un and un.group(1).lower().strip() not in [x.lower() for x in ignore]:
                    u = compareAndAlias(un.group(1), self.linenums)
                    if not u:
                        u = un.group(1)
                    special(u, unw.group(1), '')
                    self.linenums = addUn(un.group(1), self.linenums)
                elif ua and ua.group(1).lower().strip() not in [x.lower() for x in ignore]:
                    u = compareAndAlias(ua.group(1), self.linenums)
                    if not u:
                        u = ua.group(1)
                    special(u, uaw.group(1), ua.group(1) + ' ')
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

    def returnWords(self, username, line):
        if line[:len(username)].lower() != username.lower():
            return re.split("[;:\(\)@\.\s\!\?\",]+", line)
        return re.split("[;:\(\)@\.\s\!\?\",]+", line[len(username):])

    def specialFuncs(self, username, line, t):
        words = self.returnWords(username, line)
        self.countWords(username, words, t)
        self.countSwears(username, words)
        self.listLines(username, line, t)
    
    def randLines(self):
        for user in self.userlines:
            randtemp = random.choice(self.userlines[user])
            self.randomlines[user] = randtemp

    def genEverything(self):
        self.countLines(self.specialFuncs)
        self.fixListLines()
        self.randLines()
        self.commonWords()

check = Logs('', ['testlog.log'])

print "Total number of lines:", check.totallines

print "\nTotal number of lines by user:"
for u in check.linenums:
    print u + ': ' + str(check.linenums[u]) + ',',

print "\n\nUsers that never spoke, only used actions (and their number of lines):"
for u in check.actionsonly:
    print u + ': ' + str(check.actionsonly[u]) + ',',

print "\n\nTotal number of actions by user:"
for u in check.uactions:
    print u + ': ' + str(check.uactions[u]) + ',',

print "\n\nRandom lines from each user:"
for user in check.randomlines:
    print '\t' + user + ': ' + check.randomlines[user]

print "\nMost common words in the channel, and how often they were used:"
for word in check.wordlist[:15]:
    print word[0] + ': ' + str(word[1]) + ',',

print "\n\nHow often people swore with each swear:"
for u in check.swears:
    print u + ': ' + str(check.swears[u]) + ',',
