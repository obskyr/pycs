
## Comment for aliases.cfg
aliascomment = """## To add aliases for a nickname:
## Write the nickname, an equals sign ('='), a lowercase L in brackets ('[l]')
## ...and then a list of desired aliases separated by commas.

## You can, for an example, change the name of a person who isn't represented as
## what you want in the output. You can also collect all of a user's different nicknames in a single nickname."""


## Comments for settings.cfg

settings_comment        ="""## Edit this file to customize how PYCS works.
## For help with each option, read settings_help.txt.\n"""

ignored_nicks_comment   ="""## Ignored nicks:
##  Add every nickname you want to ignore in stats after the '[l]' separated by commas."""
ignored_words_comment   ="""## Ignored words:
##  Add every word you don't want to count after the '[l]' separated by commas."""
minimum_length_comment  ="""## Minimum word length:
##  The minimum number of letters in a word to be counted for stats."""
log_format_comment      ="""## Log format:
##  The name of the program you're using for IRC in lowercase letters.
##  Valid formats can be found in [your PYCS directory]/resources/formats."""
path_override_comment   ="""## Path override:
##  If you fill this in after the '[l]', PYCS will ignore any path conventions it
##  has and use the comma-separated list of directories you supplied as the
##  directory to look for logs. It is not uncommon to use this option."""
logs_parent_comment     ="""## Logs parent directories:
##  The name of the directories with your logs directory in it (eg. HexChat, mIRC).
##  Enter as comma-separated list after '[l]'. Will be overridden by Path override."""
logs_comment            ="""## Logs:
##  Enter the file names of the logs you want to analyze after the '[l]'.
##  PYCS will look for these in either the "Path override" directory or the directory it thinks your logs are in."""
print_progress_comment  ="""## Print progress:
##  Set it to True or False. If it's False, PYCS won't print its progress to
##  the console. This can be useful if you're scheduling PYCS."""
swears_comment          ="""## Swears:
##  Enter a comma-separated list of swears after the '[l]' - PYCS will count
##  those words as swears. Use '*' as joker character.
"""
settings_comments = (ignored_nicks_comment + '\n', ignored_words_comment + '\n',
                     minimum_length_comment+ '\n', log_format_comment    + '\n',
                     path_override_comment + '\n', logs_parent_comment   + '\n',
                     logs_comment          + '\n', print_progress_comment+ '\n',
                     swears_comment        + '\n'
                     )
