
import os           ## Needed to get parent directory, create directories and load logs
import confutil     ## Needed for loading and creating config
import comments     ## Needed for adding comments to config files.

try:
    pycspath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
except NameError:
    pycspath = os.path.dirname(os.getcwd())

if not os.path.exists(pycspath + '\\settings'): ## Create needed directories
    os.makedirs(pycspath + '\\settings')
if not os.path.exists(pycspath + '\\settings\\settings_help.txt'): ## Creates help file
    settings_help = open(pycspath + '\\settings\\settings_help.txt', 'w')
    for comment in comments.settings_comments:
        settings_help.write(comment + '\n')
    settings_help.close()

try:            ## Setting config variables from config file
    config = confutil.cVars(pycspath + '\\settings\\settings.cfg') 

    ignore          = config['Ignored nicks'            ]
    ignored_words   = config['Ignored words'            ]
    minlength       = abs(int(config['Minimum word length']))
    swears          = config['Swears'                   ]
    logformat       = config['Log format'               ]
    pathoverride    = config['Path override'            ]
    logdirs         = config['Logs parent directories'  ]
    lognames        = config['Logs'                     ]
    printprogress   = confutil.stringToBool(config['Print progress']) ## Don't move parenthesis
    channelname     = config['Channel name'             ]
    detailusers     = abs(int(config['Detailed users']) )
    template        = config['Theme'                    ]

    swears = [r'\b' + swear.lower().replace(r'*', r'\w*') + r'\b' for swear in swears] ## Allows joker characters

except IOError: ## Creating config file
    config = (   comments.settings_comment                                   ,
                 '## Log specifics\n'                                        ,               
                ('Log format', 'hexchat'                                    ),
                ('Logs parent directories', ['HexChat', 'AnotherIRCdir'],   ),
                ('Logs', ['Network-#Channel.log', 'Another-#Sample.log'],   ),
                ('Path override', []                                        ),
                 '\n\n## Customization\n'                                    ,
                ('Channel name', 'Channel'                                  ),
                ('Theme', 'default'                                         ),
                ('Ignored nicks', ['example?1', 'example?2']                ),
                ('Ignored words', ['ignorethis', 'andthis']                 ),
                ('Minimum word length', 4,                                  ),
                ('Swears', ['swear1', 'swear2']                             ),
                ('Detailed users', 10                                       ),
                ('Print progress', "True"                                   )
              )

    confutil.createConfig(config, pycspath + '\\settings\\settings.cfg')
    config = confutil.cVars(pycspath + '\\settings\\settings.cfg')

    ignore          = config['Ignored nicks'            ]
    ignored_words   = config['Ignored words'            ]
    minlength       = abs(int(config['Minimum word length']))
    swears          = config['Swears'                   ]
    logformat       = config['Log format'               ]
    pathoverride    = config['Path override'            ]
    logdirs         = config['Logs parent directories'  ]
    lognames        = config['Logs'                     ]
    printprogress   = confutil.stringToBool(config['Print progress']) ## Don't move parenthesis
    channelname     = config['Channel name'             ]
    detailusers     = abs(int(config['Detailed users']) )
    template        = config['Theme'                    ]

    swears = [r'\b' + swear.lower().replace(r'*', r'\w*') + r'\b' for swear in swears] ## Allows joker characters

try:            ## Loading aliases from alias file
    aliases = confutil.cVars(pycspath + '\\settings\\aliases.cfg')

except IOError: ## Creating alias file
    aliases = {'SampleNick': ['alias1', 'alias2']}
    confutil.createConfig(aliases, pycspath + '\\settings\\aliases.cfg', comments.aliascomment)

try:            ## Loading patterns dictionary
    linepatterns        = confutil.cVars(pycspath + '\\resources\\formats\\' + logformat.lower() + '.cfg')
    try:
        for key in linepatterns: ## Allows for Unicode symbols to be used
            linepatterns[key] = unicode(linepatterns[key], 'utf-8')
    except TypeError:
        pass
    pattern_said_line   = linepatterns['said line'      ]
    pattern_action_line = linepatterns['action line'    ]
    pattern_time        = linepatterns['time'           ]

except (IOError, ValueError): ## Plain error invoked by incorrect settings/filter file
    print "Invalid format file. Using defaults."
    pattern_said_line   = "^[a-zA-Z]{3}\s[0-9]+\s[0-9:]{8}\s<(?P<nickname>[A-Za-z_-\|0-9]+)>\s(?P<words>.+)"
    pattern_action_line = "^[a-zA-Z]{3}\s[0-9]+\s[0-9:]{8}\s\*\s+(?P<nickname>[A-Za-z_-\|0-9]+)\s(?P<words>.+)"
    pattern_time        = "^[a-zA-Z]{3}\s[0-9]+\s(?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}):[0-9]{2}"
