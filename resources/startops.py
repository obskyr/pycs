
import os           ## Needed to get parent directory, create directories and load logs
import confutil     ## Needed for loading and creating config
import comments     ## Needed for adding comments to config files.

pycspath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

if not os.path.exists(pycspath + '\\settings'): ## Create needed directories
    os.makedirs(pycspath + '\\settings') 

try:            ## Setting config variables from config file
    config = confutil.cVars(pycspath + '\\settings\\settings.cfg') 

    ignore          = config['Ignored nicks']
    ignored_words   = config['Ignored words']
    minlength       = int(config['Minimum word length'])
    swears          = config['Swears']
    logformat       = config['Log format']
    pathoverride    = config['Path override']
    logdirs   = config['Logs parent directories']
    lognames        = config['Logs']
    printprogress   = confutil.stringToBool(config['Print progress'])

    for n, swear in enumerate(swears):
        swears[n] = swear.lower().replace(r'*', r'.*')

except IOError: ## Creating config file
    config = {'Ignored nicks': ['example?1', 'example?2'],
              'Ignored words': ['ignorethis', 'andthis'],
              'Minimum word length': 4,
              'Swears': ['swear1', 'swear2'],
              'Log format': 'hexchat',
              'Path override': '',
              'Logs parent directories': ['HexChat', 'AnotherIRCdir'],
              'Logs': ['Network-#Channel.log', 'Another-#Sample.log'],
              'Print progress': "True"
              }

    ignore          = config['Ignored nicks']
    ignored_words   = config['Ignored words']
    minlength       = config['Minimum word length']
    swears          = config['Swears']
    logformat       = config['Log format']
    pathoverride    = config['Path override']
    logdirs         = config['Logs parent directories']
    lognames        = config['Logs']
    printprogress   = confutil.stringToBool(config['Print progress'])

    confutil.createConfig(config, pycspath + '\\settings\\settings.cfg', comments.configcomment)


try:            ## Loading aliases from alias file
    aliases = confutil.cVars(pycspath + '\\settings\\aliases.cfg')

except IOError: ## Creating alias file
    aliases = {'SampleNick': ['alias1', 'alias2']}
    confutil.createConfig(aliases, pycspath + '\\settings\\aliases.cfg', comments.aliascomment)

try:            ## Loading patterns dictionary
    linepatterns        = confutil.cVars(pycspath + '\\resources\\formats\\' + logformat.lower() + '.cfg')
    pattern_username    = linepatterns['username']
    pattern_useraction  = linepatterns['action username']
    pattern_saidwords   = linepatterns['said words']
    pattern_actionwords = linepatterns['action words']
    pattern_time        = linepatterns['time']

except (IOError, ValueError): ## Plain error with incorrect settings
    print "Invalid format file. Using defaults."
    pattern_username    = "^[a-zA-Z]{3}\s[0-9]+\s[0-9:]{8}\s<([A-Za-z_-\|0-9]+)>"
    pattern_useraction  = "^[a-zA-Z]{3}\s[0-9]+\s[0-9:]{8}\s\*\s+([A-Za-z_-\|0-9]+)\s"
    pattern_saidwords   = "^[a-zA-Z]{3}\s[0-9]+\s[0-9:]{8}\s<[A-Za-z_-\|0-9]+>(.+)"
    pattern_actionwords = "^[a-zA-Z]{3}\s[0-9]+\s[0-9:]{8}\s\*\s+[A-Za-z_-\|0-9]+\s(.+)"
    pattern_time        = "^[a-zA-Z]{3}\s[0-9]+\s([0-9]{2}):([0-9]{2}):[0-9]{2}"

try:            ## Setting time format
    timeformat = [x.lower() for x in linepatterns['time format']]
except (KeyError, NameError): ## Default time format
    timeformat = ('hour', 'minute')
hnum, mnum = timeformat.index('hour') + 1, timeformat.index('minute')
