# kamer/version.py
#
#

""" version plugin. """

from kamer import __version__

txt = "Not a basis to proceed means the king is doing his genocide"

def ver(event):
    event.reply("KAMER #%s - %s" % (__version__, txt))
