
## Comment for aliases.cfg
aliascomment = """## To add aliases for a nickname:
## Write the nickname, an equals sign ('='), a lowercase L in brackets ('[l]')
## ...and then a list of desired aliases separated by commas. Separate users with newlines.

## You can, for an example, change the name of a person who isn't represented as
## what you want in the output. You can also collect all of a user's different nicknames in a single nickname."""


## Comments for settings.cfg

settings_comment        ="""## Edit this file to customize how PYCS works.
## For help with each option, read settings_help.txt.\n"""

log_specifics_cat       ="""

--- Log specifics ---
"""
customization_cat       ="""

--- Customization ---
"""

channel_name_comment    ="""
Channel name:
 Enter the name of the channel you're analyzing (eg. "#Channel")."""
ignored_nicks_comment   ="""
Ignored nicks:
 Add every nickname you want to ignore in stats after the '[l]' separated by commas."""
ignored_words_comment   ="""
Ignored words:
 Add every word you don't want to count after the '[l]' separated by commas."""
minimum_length_comment  ="""
Minimum word length:
 The minimum number of letters in a word to be counted for stats."""
log_format_comment      ="""
Log format:
 The name of the program you're using for IRC in lowercase letters.
 Valid formats can be found in [your PYCS directory]/resources/formats."""
path_override_comment   ="""
Path override:
 If you fill this in after the '[l]', PYCS will ignore any path conventions it
 has and use the comma-separated list of directories you supplied as the
 directory to look for logs. It is not uncommon to use this option."""
logs_parent_comment     ="""
Logs parent directories:
 The name of the directories with your logs directory in it (eg. HexChat, mIRC).
 Enter as comma-separated list after '[l]'. Will be overridden by Path override."""
logs_comment            ="""
Logs:
 Enter the file names of the logs you want to analyze after the '[l]'.
 PYCS will look for these in either the "Path override" directory or the directory it thinks your logs are in."""
print_progress_comment  ="""
Print progress:
 Set it to True or False. If it's False, PYCS won't print its progress to
 the console. This can be useful if you're scheduling PYCS."""
swears_comment          ="""
Swears:
 Enter a comma-separated list of swears after the '[l]' - PYCS will count
 those words as swears. Use '*' as joker character. Leave the field empty
 after the '[l]' to not coutnt swears."""
detailed_users_comment  ="""
Detailed users:
 Enter the number of users you'd like to see detailed in the output.
 By default, the top 10 are shown."""
top_words_comment       ="""
Top words:
 Enter the number of words you'd like to appear in the "top list" of words."""
theme_comment           ="""
Theme:
 Enter the name of the theme you wish to use. Valid theme names are
 all of the folders in /resources/templates."""
show_brief_users_comment     ="""
Show brief users:
 Set to True or False. If false, PYCS will not show stats for any users beyond "Detailed users"."""
brief_users_comment ="""
Brief users:
 If "Show brief users" is set to True, this will dictate up to which number to show brief users.
 Set to 0 to show all. If less than "Detailed users", none will be shown."""
settings_comments = (
    log_specifics_cat,
    
    log_format_comment,
    logs_parent_comment,
    logs_comment,
    path_override_comment,

    customization_cat,

    channel_name_comment,
    theme_comment,
    ignored_nicks_comment,
    ignored_words_comment,
    detailed_users_comment,
    show_brief_users_comment,
    brief_users_comment,
    minimum_length_comment,
    top_words_comment,
    swears_comment,
    print_progress_comment
    )
