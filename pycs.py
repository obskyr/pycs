import os
import sys

sys.path.insert(0, os.getcwd() + r"\resources")

import confutil
import generate

userdir = os.path.expanduser('~')
logpaths = ['logs', 'xchatlogs']

if not os.path.exists('output'):
    os.makedirs('output')

if not generate.pathoverride.strip():
    ircpaths = {
        'hexchat': ['HexChat'],
        'xchat': ['xchat', 'X-Chat 2'],
        'custom': []
        } 
    config = {'ircapp': 'hexchat', 'outputdir': 'output', 'ircdir': ircpaths}
    createConfig(config, 'pycs.cfg')
    ircapp = config['ircapp']
    ircdir = ircpaths[ircapp]
    outputdir = config['outputdir']
    
if os.name == 'nt':
    appdpath = os.environ['APPDATA']
    ircpath = appdpath + '\\' + ircdir
