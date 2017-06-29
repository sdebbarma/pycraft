__author__ = 'sbarma'


# IMPORT
try :
	from selenium import webdriver
except ImportError :
	print "ERROR: UNABLE TO IMPORT SELENIUM WEBDRIVER"
	exit(1)

try :
	from ..lib import DataController
except ImportError :
	print "ERROR: UNABLE TO IMPORT DATA CONTROLLER (LOCAL)"
	exit(1)

try :
	from termcolor import cprint
except ImportError :
	print "ERROR: UNABLE TO IMPORT CPRINT"
	exit(1)

try :
	import time
except ImportError :
	print "ERROR: UNABLE TO IMPORT TIME"
	exit(1)

try :
	import datetime
except ImportError :
	print "ERROR: UNABLE TO IMPORT DATETIME"
	exit(1)

try :
	import re
except ImportError :
	print "ERROR: UNABLE TO IMPORT RE"
	exit(1)



# GUI CONTROLLER CLASS
class GUIController( object ):

	# constructor with context, browser type
	def __init__( self, context, browser_type='chrome' ):
		# set context
		self._context = context

		# exit in case of error
		if context.ERROR_NO == -1:
			if self._context.ON_ERROR_EXIT: exit(1)

		if context.BROWSER is None:
			# set browser
			if self._context.config.userdata.has_key('BROWSER_TYPE'):
				if len(self._context.config.userdata['BROWSER_TYPE']) > 0:
					browser_type = self._context.config.userdata['BROWSER_TYPE']
			
			# setup chrome as webdriver
			if browser_type.strip().lower() == "chrome":
				try:
					self._browser = webdriver.Chrome()
					self._browser.maximize_window()
				except:
					cprint("ERROR: UNABLE TO OPEN CHROME", "red")
					self._context.ERROR_DESC = "ERROR: UNABLE TO OPEN CHROME"
					self._context.ERROR_NO = -1
			elif browser_type.strip().lower() == "firefox":
				try:
					self._browser = webdriver.Firefox()
				except:
					cprint("ERROR: UNABLE TO OPEN FIREFOX", "red")
					self._context.ERROR_DESC = "ERROR: UNABLE TO OPEN FIREFOX"
					self._context.ERROR_NO = -1
			else:
				cprint("ERROR: UNABLE TO OPEN BROWSER (" + str(browser_type) + ")", "red")
				self._context.ERROR_DESC = "ERROR: UNABLE TO OPEN BROWSER (" + str(browser_type) + ")"
				self._context.ERROR_NO = -1
				self._browser = None
			
			context.BROWSER = self._browser
		else:
			self._browser = context.BROWSER


	# navigate to a website
	def navigate( self, website='' ):
		# exit in case of error
		if self._context.ERROR_NO == -1:
			if self._context.ON_ERROR_EXIT: exit(1)

		# navigate to website
		if self._browser is not None:
			if self._context.config.userdata.has_key('WEBSITE'):
				if len(self._context.config.userdata['WEBSITE']) > 0:
					website = self._context.config.userdata['WEBSITE']
			try:
				self._browser.get( website )
				step_desc = "OPENED URL (" + str(website) + ")"
				status = "DONE"
				info = {}
			
			except:
				step_desc = "ERROR: UNABLE TO OPEN URL (" + str(website) + ")"
				cprint(step_desc, "red")
				self._context.ERROR_DESC = step_desc
				self._context.ERROR_NO = -1
				status = "FAILED"
				info = {}
			
		# prepare sub-step
		dr = DataController( self._context )
		try:
			# add runtime step with name, status and info (e.g. gui element, error, etc.)
			dr.prepSubStepDetails({ \
				"DocStepName": str(step_desc), \
				"DocStepInfo": dict(info)}, status)
		except:
			pass


	# close browser instance
	def close_browser( self ):
		if self._browser is not None:
			try:
				self._browser.close()
			except:
				pass


	# highlight gui element
	def highlight_element( self, element, background ):
		if element is not None:
			self._browser.execute_script("arguments[0].setAttribute('style','background: " + str(background) + "')", element)


	# locate ui element
	def locate_element( self, name, locator, locate_by='xpath', wait_in_seconds=2, background='yellow' ):
		# exit in case of error
		if self._context.ERROR_NO == -1:
			if self._context.ON_ERROR_EXIT: exit(1)

		# locate gui element - by xpath (default), id, name, class, css, etc.
		try:
			element = None
			self.element_found = False
			if locate_by.strip().lower() == "xpath":
				element = self._browser.find_element_by_xpath( locator )
				self.element_found = True
			elif locate_by.strip().lower() == "id":
				element = self._browser.find_element_by_id( locator )
				self.element_found = True
			elif locate_by.strip().lower() == "name":
				element = self._browser.find_element_by_name( locator )
				self.element_found = True

			if self.element_found:
				self.highlight_element( element, background )
				if wait_in_seconds > 0:
					time.sleep( wait_in_seconds )

				step_desc = "LOCATED ELEMENT (" + str(name) + " by " + str(locate_by) + " as \"" + str(locator) + "\")"
				status = "DONE"
				info = {}

			else:
				step_desc = "ERROR: UNABLE TO LOCATE ELEMENT (" + str(name) + " by " + str(locate_by) + " as \"" + str(locator) + "\")"
				cprint(step_desc, "red")
				self._context.ERROR_DESC = step_desc
				self._context.ERROR_NO = -1
				status = "FAILED"
				info = {}
		
		except:
			step_desc = "ERROR: UNABLE TO LOCATE ELEMENT (" + str(name) + " by " + str(locate_by) + " as \"" + str(locator) + "\")"
			cprint(step_desc, "red")
			self._context.ERROR_DESC = step_desc
			self._context.ERROR_NO = -1
			status = "FAILED"
			info = {}

		# prepare sub-step
		dr = DataController( self._context )
		try:
			# add runtime step with name, status and info (e.g. gui element, error, etc.)
			dr.prepSubStepDetails({ \
				"DocStepName": str(step_desc), \
				"DocStepInfo": dict(info)}, status)
		except:
			pass

		# return gui element
		return element


	# enter/select/check gui element
	#def write_text( self, element, text, multi_text=False ):
	def write_text( self, element, text ):
		# exit in case of error
		if self._context.ERROR_NO == -1:
			if self._context.ON_ERROR_EXIT: exit(1)

		if element is not None:
			try:
				element.send_keys( text )
				step_desc = "WRITE TEXT (" + str(text) + ")"
				status = "DONE"
				info = {}
			
			except:
				step_desc = "ERROR: UNABLE TO WRITE TEXT (" + str(text) + ")"
				cprint(step_desc, "red")
				self._context.ERROR_DESC = step_desc
				self._context.ERROR_NO = -1
				status = "FAILED"
				info = {}

		# prepare sub-step
		dr = DataController( self._context )
		try:
			# add runtime step with name, status and info (e.g. gui element, error, etc.)
			dr.prepSubStepDetails({ \
				"DocStepName": str(step_desc), \
				"DocStepInfo": dict(info)}, status)
		except:
			pass


	# single/double click on gui element
	#def click_element( self, element, double=False ):
	def click_element( self, element ):
		# exit in case of error
		if self._context.ERROR_NO == -1:
			if self._context.ON_ERROR_EXIT: exit(1)

		if element is not None:
			try:
				element.click()
				step_desc = "CLICKED ELEMENT"
				status = "DONE"
				info = {}
			
			except:
				step_desc = "ERROR: UNABLE TO CLICK ELEMENT"
				cprint(step_desc, "red")
				self._context.ERROR_DESC = step_desc
				self._context.ERROR_NO = -1
				status = "FAILED"
				info = {}

		# prepare sub-step
		dr = DataController( self._context )
		try:
			# add runtime step with name, status and info (e.g. gui element, error, etc.)
			dr.prepSubStepDetails({ \
				"DocStepName": str(step_desc), \
				"DocStepInfo": dict(info)}, status)
		except:
			pass


	# read run-time attributes of gui element
	def read_element( self, element, attribute ):
		# exit in case of error
		if self._context.ERROR_NO == -1:
			if self._context.ON_ERROR_EXIT: exit(1)

		runtime_text = ""
		if element is not None:
			try:
				runtime_text = element.get_attribute( attribute )
				step_desc = "READ ATTRIBUTE (" + str(attribute) + ": " + str(runtime_text) + ")"
				status = "DONE"
				info = {}
			
			except:
				step_desc = "ERROR: UNABLE TO READ ATTRIBUTE (" + str(attribute) + ": " + str(runtime_text) + ")"
				cprint(step_desc, "red")
				self._context.ERROR_DESC = step_desc
				self._context.ERROR_NO = -1
				status = "FAILED"
				info = {}

		# return text
		return runtime_text

		# prepare sub-step
		dr = DataController( self._context )
		try:
			# add runtime step with name, status and info (e.g. gui element, error, etc.)
			dr.prepSubStepDetails({ \
				"DocStepName": str(step_desc), \
				"DocStepInfo": dict(info)}, status)
		except:
			pass


	# get dialog's or alert's text
	def read_dialog( self, wait_in_seconds=2 ):
		# exit in case of error
		if self._context.ERROR_NO == -1:
			if self._context.ON_ERROR_EXIT: exit(1)

		# assert text
		runtime_text = ""
		try:
			element = self._browser.switch_to_alert()
			runtime_text = element.text
			if wait_in_seconds > 0:
				time.sleep( wait_in_seconds )
			element.dismiss()
			
			step_desc = "READ DIALOG AS (" + str(runtime_text) + ")"
			status = "DONE"
			info = {}
			
		except:
			step_desc = "ERROR: UNABLE TO LOCATE/READ DIALOG (" + str(element) + ")"
			cprint(step_desc, "red")
			self._context.ERROR_DESC = step_desc
			self._context.ERROR_NO = -1
			status = "FAILED"
			info = {}

		# prepare sub-step
		dr = DataController( self._context )
		try:
			# add runtime step with name, status and info (e.g. gui element, error, etc.)
			dr.prepSubStepDetails({ \
				"DocStepName": str(step_desc), \
				"DocStepInfo": dict(info)}, status)
		except:
			pass

		return runtime_text


	# assert actual against expected
	def assert_text( self, exp_value, act_value ):
		# exit in case of error
		if self._context.ERROR_NO == -1:
			if self._context.ON_ERROR_EXIT: exit(1)

		# assert text
		try:
			assert exp_value == act_value

			step_desc = "EXPECTED vs ACTUAL (" + str(exp_value) + " == " + str(act_value) + ")"
			status = "PASSED"
			info = {}
			
		except:
			step_desc = "ERROR: EXPECTED vs ACTUAL (" + str(exp_value) + " != " + str(act_value) + ")"
			cprint(step_desc, "red")
			self._context.ERROR_DESC = step_desc
			self._context.ERROR_NO = -1
			status = "FAILED"
			info = {}

		# prepare sub-step
		dr = DataController( self._context )
		try:
			# add runtime step with name, status and info (e.g. gui element, error, etc.)
			dr.prepSubStepDetails({ \
				"DocStepName": str(step_desc), \
				"DocStepInfo": dict(info)}, status)
		except:
			pass
