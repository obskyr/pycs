aliascomment = """## To add aliases for a nickname:
## Write the nickname, an equals sign ('='), a lowercase L in brackets ('[l]')
## ...and then a list of desired aliases separated by commas.

## You can, for an example, change the name of a person who isn't represented as
## what you want in the output. You can also collect all of a person's different nicknames in a single nickname."""

configcomment = """## Information about each option:
##
##  Ignored nicks:
##\tAdd every nickname you want to ignore in stats after the '[l]' separated by commas.
##
##  Ignored words:
##\tAdd every word you don't want to count after the '[l]' separated by commas.
##
##  Minimum word length:
##\tThe minimum number of letters in a word to be counted for stats.
##
##  Log format:
##\tThe name of the program you're using for IRC in lowercase letters. Valid formats can be found in [your PYCS directory]/resources/formats.
##
##  Path override:
##\tIf you fill this in, PYCS wil ignore any path conventions it has and use the one you supplied as the directory to look for logs.
##
##  Logs directory:
##\tThe name of the directory with your logs in it (eg. HexChat, mIRC). Will be overridden by Path override.
##
##  Logs:
##\tEnter the file names of the logs you want to analyze after the '[l]'. PYCS will look for these in either the "Path override" directory or the directory it thinks your logs are in.
"""
