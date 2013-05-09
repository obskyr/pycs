# -*- coding: cp1252 -*-
def cVars(confile):
    """Returns a dictionary with the keys and values specified in a separate config file."""
    configs = open(confile, 'r')
    cf = {}
    for line in [l for l in configs if l and l[0:2] != '##' and l != '\n']:
        key, value = line.split("=")
        if not value.strip()[0:3] == '[l]':
            cf[key.strip()] = value.strip()
        else:
            value = [e.strip() for e in value.strip()[3:].split(',')]
            cf[key.strip()] = value
    configs.close()
    return cf

def createConfig(defdict, filename, beforecomment='', aftercomment=''):
    """Creates a config file 'filename' based on dictionary 'defdict'."""
    confile = open(filename, 'w') ##vpmgoöe
    if beforecomment:
        confile.write(str(beforecomment) + '\n')
    for key in defdict.keys():
        if not type(defdict[key]) == list:
            confile.write(str(key) + "\t\t=\t" + str(defdict[key]) + "\n")
        else:
            confile.write(str(key) + "\t\t=\t[l] " + ', '.join(defdict[key]).strip() + "\n")
    if aftercomment:
        confile.write(str(aftercomment) + '\n')
    confile.close()
    lineSort(filename)

def lineSort(filename):
    """Sorts the lines in file 'filename' alphabetically."""
    sortfile = open(filename, 'r')
    lines = sortfile.read().split('\n')
    nonempty = [line.rstrip() for line in lines if line.strip() and line.strip()[0:2] != '##']
    beforecomments = []
    aftercomments = []
    for line in lines:
        if line[0:2] == '##':
            beforecomments.append(line)
        else:
            break
    for line in lines[::-1]:
        if line[0:2] == '##':
            aftercomments.append(line)
        else:
            break
    if beforecomments == aftercomments:
        aftercomments = []
    nonempty.sort()
    sortfile.close()
    sortfile = open(filename, 'w')
    sortfile.write('\n'.join(beforecomments) + '\n\n' + '\n'.join(nonempty) + '\n' + '\n\n'.join(aftercomments) + '\n')
    sortfile.close()

def stringToBool(s):
    return s.lower() == 'true'
