import unittest, os

# Set environment variables
os.environ['SPLUNK_SOURCE'] = "841154226728"
os.environ['SPLUNK_EVENT_TYPE'] = "metric"
os.environ['SPLUNK_HOST'] = "841154226728"
os.environ['SPLUNK_INDEX'] = "aws"

import importlib
lambda_module = importlib.import_module('lambda')


class CloudWatchMetrics_Firehose_Resources_Tests(unittest.TestCase):


	def test_parseEventAsMetric(self):

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


	def test_integration_metric(self):

		# Read in test inputs
		test_input = []
		with open('test_fixtures_integration_metric_events.txt') as test_fixtures_integration_metric_events:
			test_input = test_fixtures_integration_metric_events.readlines()

		# Read in test outputs
		test_output = []
		with open('test_fixtures_integration_metric_returnRecords.txt') as test_fixtures_integration_metric_returnRecords:
			test_output = test_fixtures_integration_metric_returnRecords.readlines()

		testRange = range(len(test_input))
		for i in testRange:

			testInput = eval(test_input[i])
			testOutput = eval("{'records': " + test_output[i]+ "}")

			self.assertEqual(lambda_module.handler(testInput, "none"), testOutput)


if __name__ == '__main__':
	unittest.main()