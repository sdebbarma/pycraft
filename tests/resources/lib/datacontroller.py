__author__ = 'sbarma'


# IMPORT
try :
	from termcolor import cprint
except ImportError :
	print "ERROR: UNABLE TO IMPORT CPRINT"
	exit(1)

try :
	from selenium import webdriver
except ImportError :
	print "ERROR: UNABLE TO IMPORT SELENIUM WEBDRIVER"
	exit(1)

try :
	from ..lib import DataClient
except ImportError :
	print "ERROR: UNABLE TO IMPORT DATA CLIENT (LOCAL)"
	exit(1)

try :
	from bson import json_util
except ImportError :
	print "ERROR: UNABLE TO IMPORT JSON UTIL"
	exit(1)

try :
	import os
except ImportError :
	print "ERROR: UNABLE TO IMPORT OS"
	exit(1)

try :
	import json
except ImportError :
	print "ERROR: UNABLE TO IMPORT JSON"
	exit(1)

try :
	import datetime
except ImportError :
	print "ERROR: UNABLE TO IMPORT DATETIME"
	exit(1)



# MONGODB DATA CONTROLLER CLASS
class DataController:

	# constructor with context
	def __init__(self, context):
		self._context = context

	def initCollections(self):
		self._context.current_doc = {}
		self._context.current_run = {}

	def prepFeatureDetails(self, feature):
		self._context.feature_name = str(feature.name)

	def getOutline(self, column):
		return self._context.active_outline[column]
	
	def prepScenarioDetails(self, scenario):
		# initialize test scenario/run		
		outline = []
		self._context.steps = []
		self._context.current_doc = {}
		self._context.current_run = {}
		self._context.run_start_time = datetime.datetime.now()
		self._context.step_start_time = datetime.datetime.now()
		self._context.run_step_id = 0
		self._context.run_steps = []
		self._context.curr_refid = ''
		self._context.step_id = 0
		
		# prepare ref-id, description and status (based on outline)
		for key in self._context.active_outline.headings:
			value = self._context.active_outline[key]
			outline.append(dict({"DocDataColumn": str(key), "DocDataValue": str(value)}))
			
			if key.upper() == "REFID":
				self._context.current_doc.update({"DocRefId": str(value)})
				self._context.current_run.update({"DocRefId": str(value), "DocStatus": "NO-RUN"})
				self._context.curr_refid = str(value)
			
			if key.upper() == "DESC":
				self._context.current_doc.update({"DocDescription": str(value)})
				self._context.current_run.update({"DocDescription": str(value)})
			
			if key.upper() == "DEV" and value.upper() == "Y":
				self._context.current_doc.update({"DocStatus": "POSTED"})
				self._context.DEV = "Y"

			if key.upper() == "DEV" and value.upper() == "X":
				self._context.current_doc.update({"DocStatus": "INACTIVE"})
				self._context.DEV = "X"
			
			if key.upper() == "MAP" and value.upper() == "Y":
				self._context.current_doc.update({"DocStatus": "MAPPED"})
				self._context.MAP = "Y"

		# prepare outline data
		try:
			self._context.current_doc.update({"DocOutlineData": outline})
		except:
			err_desc = "ERROR: UNABLE TO PREPARE OUTLINE AGAINST REFID: " + str(self._context.curr_refid)
			cprint(err_desc, "red")
			self._context.ERROR_DESC = err_desc
			self._context.ERROR_NO = -1

		# prepare feature details
		try:
			self._context.current_doc.update({"DocFeature": self._context.feature_name})
		except:
			err_desc = "ERROR: UNABLE TO PREPARE FEATURE AGAINST REFID: " + str(self._context.curr_refid)
			cprint(err_desc, "red")
			self._context.ERROR_DESC = err_desc
			self._context.ERROR_NO = -1

		# prepare test scenario name
		try:
			self._context.current_doc.update({"DocName": str(scenario.name)})			
		except:
			err_desc = "ERROR: UNABLE TO PREPARE SCENARIO NAME AGAINST REFID: " + str(self._context.curr_refid)
			cprint(err_desc, "red")
			self._context.ERROR_DESC = err_desc
			self._context.ERROR_NO = -1
		
		# prepare created date-time
		timestamp = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
		rundate = datetime.datetime.today().strftime('%Y-%m-%d')
		try:
			self._context.current_doc.update({"DocDesigner": os.getenv('USERNAME'), "DocDesignedOn": str(timestamp)})
		except:
			err_desc = "ERROR: UNABLE TO PREPARE DESIGNED BY & DESIGNED ON AGAINST REFID: " + str(self._context.curr_refid)
			cprint(err_desc, "red")
			self._context.ERROR_DESC = err_desc
			self._context.ERROR_NO = -1

		try:
			self._context.current_run.update({"DocName": str(scenario.name)})			
			self._context.current_run.update({ \
				"DocExecutor": os.getenv('USERNAME'), \
				"DocExecutedOn": str(timestamp), \
				"DocDuration": "" \
			})
		except:
			err_desc = "ERROR: UNABLE TO PREPARE EXECUTED BY & EXECUTED ON AGAINST REFID: " + str(self._context.curr_refid)
			cprint(err_desc, "red")
			self._context.ERROR_DESC = err_desc
			self._context.ERROR_NO = -1

		# prepare owner, category and frequency (based on test scenario tags)
		tags = [tag.upper() for tag in scenario.tags]
		owners = self._context.config.userdata['OWNER']
		categories = self._context.config.userdata['CATEGORY']
		frequencies = self._context.config.userdata['FREQUENCY']
		self._context.current_doc.update({"DocOwner": [i for i in tags if i in owners]})
		self._context.current_doc.update({"DocCategory": [i for i in tags if i in categories]})
		self._context.current_doc.update({"DocFrequency": [i for i in tags if i in frequencies]})


	def prepStepDetails(self, step):
		# prepare step details
		try:
			self._context.step_id = self._context.step_id + 1
			self._context.steps.append({ \
				"DocStepId": str(self._context.step_id), \
				"DocStepDetails": { \
					"DocStepName": str(step.name) \
					} \
				})

			self._context.run_step_id = self._context.run_step_id + 1
			
			self._context.run_steps.append({ \
				"DocStepId": str(self._context.run_step_id), \
				"DocStepDetails": {"DocStepName": str(step.name), "DocStepInfo": {}}, \
				"DocStepDuration": "", \
				"DocStepStatus": "" \
			})
			self._context.run_substep_id = 0
		except:
			err_desc = "ERROR: UNABLE TO PREPARE STEP AGAINST REFID: " + str(self._context.curr_refid)
			cprint(err_desc, "red")
			self._context.ERROR_DESC = err_desc
			self._context.ERROR_NO = -1


	def prepSubStepDetails(self, substep_dict, status):
		# prepare sub-step details
		try:
			self._context.run_substep_id = self._context.run_substep_id + 1
			duration = (datetime.datetime.now() - self._context.run_start_time).total_seconds()

			self._context.steps.append({ \
				"DocStepId": str(self._context.step_id) + "_" + str(self._context.run_substep_id), \
				"DocStepDetails": dict(substep_dict), \
				"DocStepDuration": str(duration), \
				"DocStepStatus": str(status) \
			})

			self._context.current_run.update({
				"DocStatus": str(status), \
				"DocDuration": str(duration) \
			})
		
		except:
			err_desc = "ERROR: UNABLE TO PREPARE SUB-STEP AGAINST REFID: " + str(self._context.curr_refid)
			cprint(err_desc, "red")
			self._context.ERROR_DESC = err_desc
			self._context.ERROR_NO = -1
		

	def postDocument(self):
		# add steps to scenario
		try:
			self._context.current_doc.update({"DocSteps": self._context.steps})
		except:
			err_desc = "ERROR: UNABLE TO ADD STEP AGAINST REFID: " + str(self._context.curr_refid)
			cprint(err_desc, "red")
			self._context.ERROR_DESC = err_desc
			self._context.ERROR_NO = -1

		# add scenario to docs collection
		try:
			if len(self._context.current_doc) > 0 and self._context.DEV == "Y":
				db = DataClient(self._context.config.userdata['DATABASE'])
				db.getTable("docs").update({
					"DocRefId": str(self._context.curr_refid)}, \
					{"$set": dict(self._context.current_doc)}, \
					upsert=True)
		except:
			err_desc = "ERROR: UNABLE TO UPSERT INTO DOCS COLLECTION AGAINST REFID: " + str(self._context.curr_refid)
			cprint(err_desc, "red")
			self._context.ERROR_DESC = err_desc
			self._context.ERROR_NO = -1


	def postDatamap(self, test_data):
		# prepare test data (datamap)
		try:
			datamap = []
			if test_data is not None:
				for row in test_data:
					if row['DocRefId'] == self._context.curr_refid:
						datamap = json.loads(json_util.dumps(row["DocDataMap"]))
			
			if len(datamap) > 0:
				db = DataClient(self._context.config.userdata['DATABASE'])
				db.getTable("docs").update({ \
					"DocRefId": str(self._context.curr_refid)}, \
					{"$set": {"DocDataMap": list(datamap)}}, \
					upsert=True)
				db.getTable("datamap").update({ \
					"DocRefId": str(self._context.curr_refid)}, \
					{"$set": {"DocDataMap": list(datamap)}}, \
					upsert=True)
		except:
			err_desc = "ERROR: UNABLE TO UPSERT INTO DATAMAP COLLECTION AGAINST REFID: " + str(self._context.curr_refid)
			cprint(err_desc, "red")
			self._context.ERROR_DESC = err_desc
			self._context.ERROR_NO = -1


	def getParamValue(self, column_name):
		# get parameter value of the current scenario
		try:
			db = DataClient(self._context.config.userdata['DATABASE'])
			doc_cursor = db.getTable("datamap").find({"DocRefId": str(self._context.curr_refid)})
			curr_document = json.loads(json_util.dumps(doc_cursor))
			datamap = json.loads(json_util.dumps(curr_document[0]['DocDataMap']))
			
			for row in datamap:
				if row['Name'] == column_name:
					return row['Value']
		except:
			err_desc = "ERROR: UNABLE TO FIND DATA AGAINST REFID: " + str(self._context.curr_refid)
			cprint(err_desc, "red")
			self._context.ERROR_DESC = err_desc
			self._context.ERROR_NO = -1
		
		return ""


	def postRun(self):
		# add steps to test run
		try:
			self._context.current_run.update({"DocSteps": self._context.steps})			
		except:
			err_desc = "ERROR: UNABLE TO ADD STEP AGAINST REFID: " + str(self._context.curr_refid)
			cprint(err_desc, "red")
			self._context.ERROR_DESC = err_desc
			self._context.ERROR_NO = -1

		# add scenario to runs collection
		try:
			if len(self._context.current_run) > 0 and self._context.DEV == "Y":
				db = DataClient(self._context.config.userdata['DATABASE'])
				db.getTable("runs").insert(dict(self._context.current_run))
		except:
			err_desc = "ERROR: UNABLE TO UPSERT INTO DOCS COLLECTION AGAINST REFID: " + str(self._context.curr_refid)
			cprint(err_desc, "red")
			self._context.ERROR_DESC = err_desc
			self._context.ERROR_NO = -1
