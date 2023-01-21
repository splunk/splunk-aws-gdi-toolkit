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

	def test_integration_event(self):

		# Read in test inputs
		test_input = []
		with open('test_fixtures_integration_event_events.txt') as test_fixtures_integration_event_events:
			test_input = test_fixtures_integration_event_events.readlines()

		# Read in test outputs
		test_output = []
		with open('test_fixtures_integration_event_returnRecords.txt') as test_fixtures_integration_event_returnRecords:
			test_output = test_fixtures_integration_event_returnRecords.readlines()

		testRange = range(len(test_input))
		for i in testRange:

			testInput = eval(test_input[i])
			testOutput = eval("{'records':" + test_output[i]+ "}")

			self.assertEqual(lambda_module.handler(testInput, "none"), testOutput)


if __name__ == '__main__':
	unittest.main()