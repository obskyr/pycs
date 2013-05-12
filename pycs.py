import os
import confutil

userdir = os.path.expanduser('~')
logpaths = ['logs', 'xchatlogs']

if not os.path.exists('output'):
    os.makedirs('output')

try:
    config = confutil.loadConfig('pycs.cfg')
    ircapp = config['ircapp']
    outputdir = config['outputdir']
    ircpaths = config['ircpaths']
    try:
        ircdir = ircpaths[ircapp]
    except IndexError:
        print "Invalid IRC app."
        raw_input()
        quit
except IOError:
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
