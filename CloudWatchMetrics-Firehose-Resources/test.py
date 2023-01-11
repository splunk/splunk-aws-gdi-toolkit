import unittest, os

# Set environment variables
os.environ['SPLUNK_SOURCE'] = "841154226728"
os.environ['SPLUNK_EVENT_TYPE'] = "event"
os.environ['SPLUNK_HOST'] = "841154226728"
os.environ['SPLUNK_INDEX'] = "aws"

import importlib
lambda_module = importlib.import_module('lambda')


class CloudWatchMetrics_Firehose_Resources_Tests(unittest.TestCase):


	def test_parseEventAsEvent(self):

		# Read in test inputs
		test_input = []
		with open('test_fixtures_parseEventAsEvent_messages.txt') as test_fixtures_parseEventAsEvent_messages:
			test_input = test_fixtures_parseEventAsEvent_messages.readlines()

		# Read in test outputs
		test_output = []
		with open('test_fixtures_parseEventAsEvent_returns.txt') as test_fixtures_parseEventAsEvent_returns:
			test_output = test_fixtures_parseEventAsEvent_returns.readlines()

		testRange = range(len(test_input))
		for i in testRange:

			testInput = test_input[i]
			testOutput = test_output[i]

			self.assertEqual(lambda_module.parseEventAsEvent(testInput), testOutput[:-1])


	def test_parseEventAsMetric(self):

		os.environ['SPLUNK_EVENT_TYPE'] = "metric"

		# Read in test inputs
		test_input = []
		with open('test_fixtures_parseEventAsMetric_messages.txt') as test_fixtures_parseEventAsMetric_messages:
			test_input = test_fixtures_parseEventAsMetric_messages.readlines()

		# Read in test outputs
		test_output = []
		with open('test_fixtures_parseEventAsMetric_returns.txt') as test_fixtures_parseEventAsMetric_returns:
			test_output = test_fixtures_parseEventAsMetric_returns.readlines()

		testRange = range(len(test_input))
		for i in testRange:

			testInput = test_input[i]
			testOutput = test_output[i]

			self.assertEqual(lambda_module.parseEventAsMetric(testInput), testOutput[:-1])


if __name__ == '__main__':
	unittest.main()