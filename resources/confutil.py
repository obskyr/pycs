# -*- coding: UTF-8 -*-

import codecs ## Encoding is a nightmare that never ends

def cVars(confile):
    """Returns a dictionary with the keys and values specified in a separate config file."""
    configs = open(confile, 'r')
    cf = {}
    lines = [l for l in configs if l and l[:2] != '##' and l.strip()]
    if lines[0].startswith(codecs.BOM_UTF8): ## Byte order markers sometimes are interpreted as characters
        lines[0] = lines[0][len(codecs.BOM_UTF8):]
        if lines[0][:2] == '##' or not lines[0].strip():
            del lines[0]
        lines = [unicode(line, 'utf-8') for line in lines]
    for line in lines:
        key, value = line.split("=")
        if not value.strip()[0:3] == '[l]':
            cf[key.strip()] = value.strip()
        else:
            value = [e.strip() for e in value.strip()[3:].split(',')]
            cf[key.strip()] = value
    configs.close()
    return cf

def tabCount(key):
    if   len(key) >= 24:
        return ''
    elif len(key) >= 16:
        return '\t' * 1
    elif len(key) >=  8:
        return '\t' * 2
    else:
        return '\t' * 3

def createConfig(config, filename):
    """Creates a config file 'filename' based on a dictionary or tuple/list."""
    confile = open(filename, 'w') ##vpmgoöe
    if type(config) == dict:
        for key in config.keys():
            tabs = tabCount(key)
            if not type(config[key]) == list:
                confile.write(str(key) + tabs + '=\t' + str(config[key]) + '\n')
            else:
                confile.write(str(key) + tabs + '=\t[l] ' + ', '.join(config[key]).strip() + "\n")
        lineSort(filename)
    else:
        for pair in config:
            if type(pair) == str or type(pair) == unicode:
                confile.write(pair + '\n')
            else:
                key = str(pair[0])
                if type(pair[1]) == list:
                    value = str(', '.join(pair[1]))
                    value = '[l] ' + value
                else:
                    value = str(pair[1])
                tabs = tabCount(key)
                confile.write(key + tabs + '=\t' + value + '\n')
    confile.close()

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
