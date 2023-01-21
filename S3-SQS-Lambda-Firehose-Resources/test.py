import unittest, os, importlib


class CloudWatchMetrics_Firehose_Resources_Tests(unittest.TestCase):

	def setUp(self):
			# Set environment variables
			os.environ['firehoseDeliverySreamName'] = "main"
			os.environ['AWS_REGION'] = "main"
			os.environ['SPLUNK_INDEX'] = "main"
			os.environ['SPLUNK_TIME_PREFIX'] = "main"
			os.environ['SPLUNK_EVENT_DELIMITER'] = "main"
			os.environ['SPLUNK_TIME_DELINEATED_FIELD'] = "main"
			os.environ['SPLUNK_TIME_FORMAT'] = "main"
			os.environ['SPLUNK_STRFTIME_FORMAT'] = "main"
			os.environ['SPLUNK_SOURCETYPE'] = "main"
			os.environ['SPLUNK_SOURCE'] = "main"
			os.environ['SPLUNK_HOST'] = "main"
			os.environ['SPLUNK_JSON_FORMAT'] = "main"
			os.environ['SPLUNK_IGNORE_FIRST_LINE'] = "main"
			os.environ['SPLUNK_CSV_TO_JSON'] = "main"
			os.environ['SPLUNK_REMOVE_EMPTY_CSV_TO_JSON_FIELDS'] = "main"


	def test_createDdelimiter(self):
		
		lambda_module = importlib.import_module('lambda')

		self.assertEqual(lambda_module.createDelimiter("none"), "none")
		self.assertEqual(lambda_module.createDelimiter("main"), "main")
		self.assertNotEqual(lambda_module.createDelimiter("none"), " ")
		self.assertEqual(lambda_module.createDelimiter("comma"), ",")
		self.assertEqual(lambda_module.createDelimiter("space"), " ")
		self.assertEqual(lambda_module.createDelimiter("tab"), "	")
		self.assertEqual(lambda_module.createDelimiter("semicolon"), ";")

if __name__ == '__main__':
	unittest.main()