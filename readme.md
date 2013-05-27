##Visions of grandeur
PYCS will in the future hopefully be a [PISG](http://pisg.sourceforge.net/)-like Python IRC statistics generator.

It will take log files (in different formats, with the ability to supply your own) and generate different interesting statistics based on them. It will then, probably, present these statistics in an aesthetically pleasing HTML file.

It will not require any specific input past setup, so it will easily be able to be scheduled without complications.

##Usage
If you'd like to try it, you can supply a log file and see the results in text form using `gen-test.py`.

You can also try using what will be the main program - `pycs.py` - with the correct settings. Without using `Path override`, this currently only works on Windows, but if you supply your own paths it should work just fine. `pycs.py` outputs a HTML file - see the HTML output section.

In order to create the config files without generating any stats, run `startops.py` in `resources`. This allows you to modify `settings.cfg` and `aliases.cfg` before the first run.

You can create your own log format parser easily using the instructions in `\resources\formats\creation.txt`.

###HTML output
Using `pycs.py` with the correct settings will produce an `index.html` file in the `output` directory. In order to use this on your site, simply put the `index.html` file and `resources` directory (the one located in `output`, not in the main PYCS directory) somewhere on your server (using FTP, SFTP, SCP or what have you) and you're all set to access it.

To add your own flavor, you can easily make your own `stylesheet.css`, and supply your own resources.

###Oh, and...
I'm not really known for how good I am at finishing what I've started. There's always the risk I will abandon this project, and in several years look back on it and cry.