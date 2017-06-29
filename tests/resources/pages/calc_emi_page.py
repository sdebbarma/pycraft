__author__ = 'sbarma'

from resources.lib import GUIController
from termcolor import cprint


class CalcEmiPage( GUIController ):
	
	# constructor
	def __init__( self, context, browser_type='' ):
		GUIController.__init__( self, context, browser_type )

	# uimap
	uimap = {
		"LOAN AMOUNT":	"//input[@name='lnAmount']",
		"RATE":			"//input[@name='lnRate']",
		"TERM":			"//select[@name='lnTerm']",
		"PAYABLE EMI":	"//input[@name='lnPayment']",
		"CALCULATE":	"//input[@name='Calculate']",
		"CLEAR":		"//input[@name='Clear']"
	}


	# methods
	def provide_loan_details( self, amount, rate, term ):
		element = self.locate_element( "LOAN AMOUNT", self.uimap["LOAN AMOUNT"] )
		self.write_text( element, amount )		
		element = self.locate_element( "RATE", self.uimap["RATE"], "xpath", 3 )
		self.write_text( element, rate )		
		element = self.locate_element( "TERM", "lnTerm", "name" )
		self.write_text( element, term )
		

	def calculate_emi( self ):
		element = self.locate_element( "CALCULATE", "//input[@name='Calculate']", "xpath" )
		self.click_element( element )
		

	def assert_payable_emi( self, emi ):
		element = self.locate_element( "PAYABLE EMI", "lnPayment", "name", 1, "red" )
		value = self.read_element( element, "value" )
		self.assert_text( emi, value )
		

	def assert_emi_alert( self, msg ):
		text = self.read_dialog()
		self.assert_text( msg, text )
