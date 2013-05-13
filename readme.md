##Visions of grandeur
PYCS will in the future hopefully be a [PISG](http://pisg.sourceforge.net/)-like Python IRC statistics generator.

It will take log files (in different formats, and you will eventually be able to supply your own) and generate different interesting statistics based on them. It will then, probably, present these statistics in an aesthetically pleasing HTML file.

It will not require any specific input past setup, so it will easily be able to be scheduled without complications.

##Usage
Currently, the program cannot be used to generate any HTML files. If you'd really like to, you can supply a log file and see the results in Python-compliant form using `gen-test.py`, if you rename it to `testlog.log` and put it in the PYCS directory. The script doing all the work is `generate.py`.

In order to create the config files without generating any stats, run `startops.py` in `resources`. This allows you to modify `settings.cfg` and `aliases.cfg` before the first run.

You can also try using what will be the main program - `pycs.py` - with the correct settings. Without using `Path override`, this currently only works on Windows, but if you supply your own paths it should work just fine.

You can create your own log format parser easily using the instructions in `\resources\formats\creation.txt`.

###Oh, and...
I'm not really known for how good I am at finishing what I've started. There's always the risk I will abandon this project, and in several years look back on it and cry.