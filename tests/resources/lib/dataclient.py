__author__ = 'sbarma'


# IMPORT
try :
	from pymongo import MongoClient
except ImportError :
	print "ERROR: UNABLE TO IMPORT PYMONGO CLIENT"
	exit(1)



# MONGODB DATA CLIENT
class DataClient:

	# constructor with database name, host, port
	def __init__(self, dbname, host='localhost', port=27017):
		try:
			self._msg = ""
			self._conn = MongoClient(host, port)			
		except:
			self._is_connected = False
			self._msg = "MongoDB not running"
			self._conn = None
		
		if self._conn is not None:
			try:
				self._db = self._conn[dbname]
				self._is_connected = True
			except:
				self._msg = "No database with name \'" + dbname + "\'"
				self._is_connected = False

				
	# check database connection
	def isConnected(self):
		if self._is_connected:
			return self._is_connected
		else:
			self._msg = "MongoDB not connected"


	def getTable(self, cname=""):
		if self._db is not None:
			if self._is_connected:
				try:
					return self._db[cname]
				except:
					self._msg = "No collection with name \'" + cname + "\'"
			else:
				self._msg = "MongoDB not connected"
		else:
			self._msg = "MongoDB not running"
		return None


	def getMessage(self):
		return self._msg