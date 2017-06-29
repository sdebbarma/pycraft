__author__ = 'sbarma'

from resources.lib import GUIController
from termcolor import cprint


class HomePage( GUIController ):

	# constructor
	def __init__( self, context, browser_type='' ):
		GUIController.__init__( self, context, browser_type )

	# uimap
	uimap = {
		"IDBI LOGO": "//img[@src='images/idbi-bank-top.gif']"
	}
