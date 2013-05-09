
import os           ## Needed to get parent directory, create directories and load logs
import confutil     ## Needed for loading and creating config
import comments     ## Needed for adding comments to config files.

pycspath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

if not os.path.exists(pycspath + '\\settings'): ## Create needed directories
    os.makedirs(pycspath + '\\settings') 

try:            ## Setting config variables from config file
    config = confutil.cVars(pycspath + '\\settings\\settings.cfg') 
    ignore = config['Ignored nicks']
    ignored_words = config['Ignored words']
    minlength = int(config['Minimum word length'])
    swears = config['Swears']
    for n, swear in enumerate(swears):
        swears[n] = swear.lower().replace(r'*', r'.*')

except IOError: ## Creating config file
    config = {'Ignored nicks': ['example?1', 'example?2'],
              'Ignored words': ['ignorethis', 'andthis'],
              'Minimum word length': 4,
              'Swears': ['swear1', 'swear2']}
    ignore = config['Ignored nicks']
    ignored_words = config['Ignored words']
    minlength = config['Minimum word length']
    confutil.createConfig(config, pycspath + '\\settings\\settings.cfg', comments.configcomment)


try:            ## Loading aliases from alias file
    aliases = confutil.cVars(pycspath + '\\settings\\aliases.cfg')

except IOError: ## Creating alias file
    aliases = {'SampleNick': ['alias1', 'alias2']}
    confutil.createConfig(aliases, pycspath + '\\settings\\aliases.cfg', comments.aliascomment)
