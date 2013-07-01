##What is PYCS?
PYCS is a PYthon Chat Statistics generator.

It takes IRC log files and generates different interesting statistics based on them. It then presents these statistics in a visually pleasing HTML file.

It does not require any specific input past setup, and is as such very easily scheduled.

##Usage
After installing [Python](http://python.org/) and downloading PYCS, the first thing to do is run `startops.py`, which is located in the `/resources` directory. Once this is done, a folder named `settings` will be placed in your PYCS directory. Following the instructions in `settings_help.txt`, modify `settings.cfg` and `aliases.cfg` as you see fit.

Currently, the automatic path detection only works on Windows systems. PYCS is fully able to run on any system, however, by using `Path override` in `settings.cfg` to specify the exact folders where your logs are located - just make sure to enter correct filenames in the `Logs` option.

Once you've successfully run PYCS, there will be a file named `index.html` in the `output` directory. Put this file, together with the `/output/resources` directory, in whatever directory you'd like on any web server you have access to. The statistics page is now reachable, and can easily be linked from anywhere!

##Customization

###Formats

If your IRC program's log format isn't supported by PYCS, there is quite an easy way to create your own filter. Following the instructions in `/resources/formats/creation.txt`, create your own config file for your particular IRC log format.

If you do make a new format, it would be incredibly nice of you to open an issue, make a pull request or otherwise contact me about your addition and I'll be more than happy to add it to the default formats!

###Themes

PYCS fully supports making your own themes (that means completely different page layouts, not just color schemes). For information on how to do this, refer to `creation.txt` in `/resources/themes`.

As with the formats - if you do make a theme, it'd be extremely appreciated if you submitted a pull request, an issue or otherwise contacted me in order for the theme to be included in the repository.

##Contact

If you have any questions, or anything to say, I can be reached at either [powpowd@gmail.com](mailto:powpowd@gmail.com) or [@LpSamuelm](http://twitter.com/LpSamuelm) on Twitter. To get a fast answer, Twitter is your best bet!

If you have any inquiries about or problems with PYCS, opening an issue here on GitHub is a great way to reach through about that.