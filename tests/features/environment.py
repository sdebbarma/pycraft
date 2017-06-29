__author__ = 'sbarma'


from behave import *
from termcolor import cprint
from resources.lib import DataController
import json


# open json data files (file name is hardcoded for now)
def get_test_data(context, file_name):
	try:
		with open('./features/data/' + file_name) as data_file:
			try:
				test_data = json.load(data_file)
			except:
				return None
		return test_data
	
	except:
		cprint("ERROR: UNABLE TO GET TEST DATA FROM JSON FILE: " + str(file_name), "red")
		context.ERROR_DESC = str(test_data)
		context.ERROR_NO = -1
		return None


def before_all(context):
	# initialize error
	context.ERROR_NO = 0
	context.ERROR_DESC = ""
	context.ON_ERROR_EXIT = False
	context.BROWSER = None

	dr = DataController(context)
	dr.initCollections()


def before_feature(context, feature):
	dr = DataController(context)
	dr.prepFeatureDetails(feature)


def after_feature(context, feature):
	pass


def before_scenario(context, scenario):
	# reset error
	context.ERROR_NO = 0
	context.ERROR_DESC = ""
	
	# prepare scenario details
	dr = DataController(context)
	dr.prepScenarioDetails(scenario)

	# set dev/map/run flags
	context.DEV = dr.getOutline("DEV")	# Y: Yes (insert into docs), N/BLANK: No (do nothing), X: Inactive (inactivate)
	context.MAP = dr.getOutline("MAP")	# Y: Yes (insert into datamap), N/BLANK: No (do nothing), X: Inactive (inactivate)
	context.RUN = dr.getOutline("RUN")	# Y: Yes (insert into runs), N/BLANK: No (do nothing), X: Inactive (inactivate)

	# prepare test scenario
	if context.DEV == "Y":
		dr.postDocument()

	# prepare test data
	if context.MAP == "Y":
		test_data = get_test_data(context, "testdata.json")
		dr.postDatamap(test_data)


def after_scenario(context, scenario):
	dr = DataController(context)

	# post test scenario
	if context.DEV == "Y":
		dr.postDocument()

	# prepare test data
	if context.MAP == "Y":
		test_data = get_test_data(context, "testdata.json")
		dr.postDatamap(test_data)

	# prepare test run
	if context.RUN in ["Y", "T"]:
		dr.postRun()

	#cprint(context.current_doc, "cyan")
	#cprint(context.current_run, "magenta")

def before_step(context, step):
	dr = DataController(context)

	# prepare test scenario
	if context.DEV == "Y":
		dr.prepStepDetails(step)


def after_step(context, step):
	pass


def after_all(context):
	pass
