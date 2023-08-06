# koning/version.py
#
#

"koning's version" 

from koning import __version__, __txt__

def ver(event):
    event.reply("KONING %s - %s" % (__version__, __txt__))
