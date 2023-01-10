import unittest, os

# Set environment variables
os.environ['SPLUNK_SOURCE'] = "841154226728"
os.environ['SPLUNK_SOURCETYPE'] = "aws:cloudwatchlogs"
os.environ['SPLUNK_HOST'] = "841154226728"
os.environ['SPLUNK_INDEX'] = "aws"

import importlib
lambda_module = importlib.import_module('lambda')


class CloudWatchLogs_Firehose_Resources_Tests(unittest.TestCase):

	def test_series(self):

		# Read in test inputs
		test_input = []
		with open('test_fixtures_events.txt') as test_fixtures_events:
			test_input = test_fixtures_events.readlines()

		# Read in test outputs
		test_output = []
		with open('test_fixtures_returnRecords.txt') as test_fixtures_returnRecords:
			test_output = test_fixtures_returnRecords.readlines()

		testRange = range(len(test_input))
		for i in testRange:

			testInput = eval(test_input[i])
			testOutput = eval("{'records':" + test_output[i]+ "}")

			self.assertEqual(lambda_module.handler(testInput, "none"), testOutput)


if __name__ == '__main__':
	unittest.main()