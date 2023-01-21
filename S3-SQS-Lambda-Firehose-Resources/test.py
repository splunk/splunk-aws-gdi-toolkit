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

		self.lambda_module = importlib.import_module('lambda')


	def test_createDdelimiter(self):
		
		self.assertEqual(self.lambda_module.createDelimiter("none"), "none")
		self.assertEqual(self.lambda_module.createDelimiter("main"), "main")
		self.assertNotEqual(self.lambda_module.createDelimiter("none"), " ")
		self.assertEqual(self.lambda_module.createDelimiter("comma"), ",")
		self.assertEqual(self.lambda_module.createDelimiter("space"), " ")
		self.assertEqual(self.lambda_module.createDelimiter("tab"), "	")
		self.assertEqual(self.lambda_module.createDelimiter("semicolon"), ";")

	def test_retrieveObjectInfo(self):

		self.assertEqual(self.lambda_module.retrieveObjectInfo({'messageId': '0ed4e10e-7fe3-41c8-ba7e-59b0c90826f3', 'receiptHandle': 'AQEBrbGkhIBIrdBxqc9HfoDkMkaNz7/OE4jftgDzblOgi6aY4xgKPteadRUkKhr2apF8LYVsA9dZXVxPyQM74Tb0p8hNvZojgZW39Q0w8U75Lo/URZtpq/KT/LP+NBn5AUlYHwgV2Zy/i6TAs6EkNPjPj/+VYC8fNpaPeV5cFys/2Ql5hK1PTpvewhIe2TNLMjj2BUNWycSuboa5N6n5tY0wQG84JQvceb6tGW9x5Lb/ZP/ortmAZH+Yn5iUrg0sJwdudff1WdH8xZPSR3mSttskL7sSfEHS1cGLNr1XsHz4xpmX5Mv+xpievXjLMIESaO6aNoqBmQDPlZcExBJbWEXyDWrzVrU3YeQuTYaOFKXX8sf28aROG7jxJhk9NR5TSBR3w+vmuz0tgtm0pEqLHQPiC+MSi1nJeO7NbnPcnTqwvRLotFdmhlWAYBbPYsMuAoqp', 'body': '{"Records":[{"eventVersion":"2.1","eventSource":"aws:s3","awsRegion":"us-west-2","eventTime":"2023-01-21T21:08:44.251Z","eventName":"ObjectCreated:Put","userIdentity":{"principalId":"AWS:AROAV2CJ256E23ZOBRSAF:prod.pdx.dbs.datafeeds.aws.internal"},"requestParameters":{"sourceIPAddress":"172.18.238.76"},"responseElements":{"x-amz-request-id":"81KMJ9RD5J340C2G","x-amz-id-2":"ORkLTETarSJwEOsMpQaqiVSdT8uoocAjB7tOlkVzfNMrqaGPRFHR4Jb4Pxxl9UauHUq4pgDuXZ/RZkH3BQHAlHvlDZ3C3rXj"},"s3":{"s3SchemaVersion":"1.0","configurationId":"85153fb0-1426-494e-9c4e-ffffe0ebf520","bucket":{"name":"841154226728-us-west-2-vpcflowlog","ownerIdentity":{"principalId":"A12SQTDQCD6TT5"},"arn":"arn:aws:s3:::841154226728-us-west-2-vpcflowlog"},"object":{"key":"AWSLogs/841154226728/vpcflowlogs/us-west-2/2023/01/21/841154226728_vpcflowlogs_us-west-2_fl-055401975c87952e8_20230121T2100Z_1ce1bf4b.log.gz","size":2595,"eTag":"0557d1d84c8f071523cc7d18ebf58d5a","sequencer":"0063CC545C372D5A7F"}}}]}', 'attributes': {'ApproximateReceiveCount': '1', 'SentTimestamp': '1674335325396', 'SenderId': 'AIDAJFWZWTE5KRAMGW5A2', 'ApproximateFirstReceiveTimestamp': '1674335325404'}, 'messageAttributes': {}, 'md5OfBody': '1910f3b491509daba1ceadca474a08c8', 'md5OfMessageAttributes': None, 'eventSource': 'aws:sqs', 'eventSourceARN': 'arn:aws:sqs:us-west-2:841154226728:841154226728-us-west-2-vpcflowlog-sqs-queue', 'awsRegion': 'us-west-2'}), {'bucket': '841154226728-us-west-2-vpcflowlog', 'key': 'AWSLogs/841154226728/vpcflowlogs/us-west-2/2023/01/21/841154226728_vpcflowlogs_us-west-2_fl-055401975c87952e8_20230121T2100Z_1ce1bf4b.log.gz'})

		self.assertEqual(self.lambda_module.retrieveObjectInfo({'messageId': '65dd2ea3-8dc4-42fd-a180-ac91961ea2ee', 'receiptHandle': 'AQEBGerSNcBRWgr2QMCua2Q/J0m5yeHOqgzteDgS2Hmj1ZwcmAN1jITp5M+7hBLEBkL4McwVOlJJQAbPm99HZt3AhJmLX6hSqOtF8Bm2M7uP78s02L3gU1N3/1SZheorY+HCNo7smYxXLm2uYsAU/+evxEjcZzAGUBLnXpNnwT6kiU3qWw8GQ0FTci5NmGee4lt5RJjv6j4w93xnR9XovQQ9kJhcwmavXV+J5PbTSipTecfPrZDlKCMwBP+Nkfqyt3w5amVU1jl5/joK+WaSmdLGD2Evyjd4Z+05QsuA/9s/xMsoLXbiSj43CSrhH0opLWU1m7saEHRrmZJDhe2gF4rBOB8luX2I9ZoT3xyc/jPbgo3pJSAYiOwo6GEAZMoMhKRm/hcxMteB3YtDtDh8leaIRB5++ET0ASjLi1Ms8OGuoTJrz6J5GXQTJU7Ih52Jz/PY', 'body': '{"Records":[{"eventVersion":"2.1","eventSource":"aws:s3","awsRegion":"us-west-2","eventTime":"2023-01-21T21:08:44.075Z","eventName":"ObjectCreated:Put","userIdentity":{"principalId":"AWS:AROAV2CJ256E23ZOBRSAF:prod.pdx.dbs.datafeeds.aws.internal"},"requestParameters":{"sourceIPAddress":"172.19.67.123"},"responseElements":{"x-amz-request-id":"81KR386GSPPEJ1A6","x-amz-id-2":"qDVdamIDcwxeAJOnAUm4kHvzvk2HsL5aggHiz6K7UQXNaYEJrtSbd/YbLR7xD0RpSeJDueUAFyWH02WPH9j51WFH37LjjnsQ"},"s3":{"s3SchemaVersion":"1.0","configurationId":"85153fb0-1426-494e-9c4e-ffffe0ebf520","bucket":{"name":"841154226728-us-west-2-vpcflowlog","ownerIdentity":{"principalId":"A12SQTDQCD6TT5"},"arn":"arn:aws:s3:::841154226728-us-west-2-vpcflowlog"},"object":{"key":"AWSLogs/841154226728/vpcflowlogs/us-west-2/2023/01/21/841154226728_vpcflowlogs_us-west-2_fl-055401975c87952e8_20230121T2105Z_654119f1.log.gz","size":2794,"eTag":"1891e0401175628854f10ee575e9bade","sequencer":"0063CC545C0877B5E6"}}}]}', 'attributes': {'ApproximateReceiveCount': '1', 'SentTimestamp': '1674335325366', 'SenderId': 'AIDAJFWZWTE5KRAMGW5A2', 'ApproximateFirstReceiveTimestamp': '1674335325369'}, 'messageAttributes': {}, 'md5OfMessageAttributes': None, 'md5OfBody': 'b3cf3151132d06b8b68cdc64ad833dd6', 'eventSource': 'aws:sqs', 'eventSourceARN': 'arn:aws:sqs:us-west-2:841154226728:841154226728-us-west-2-vpcflowlog-sqs-queue', 'awsRegion': 'us-west-2'}), {'bucket': '841154226728-us-west-2-vpcflowlog', 'key': 'AWSLogs/841154226728/vpcflowlogs/us-west-2/2023/01/21/841154226728_vpcflowlogs_us-west-2_fl-055401975c87952e8_20230121T2105Z_654119f1.log.gz'})

		self.assertEqual(self.lambda_module.retrieveObjectInfo({'messageId': '0ed4e10e-7fe3-41c8-ba7e-59b0c90826f3', 'receiptHandle': 'AQEBrbGkhIBIrdBxqc9HfoDkMkaNz7/'}), "SQS message did not contain S3 file information.  Record: {'messageId': '0ed4e10e-7fe3-41c8-ba7e-59b0c90826f3', 'receiptHandle': 'AQEBrbGkhIBIrdBxqc9HfoDkMkaNz7/'}")

	def test_validateFileType(self):
		
		self.assertEqual(self.lambda_module.validateFileType("none"), "Unsupported file type.")
		self.assertEqual(self.lambda_module.validateFileType("841154226728_vpcflowlogs_us-west-2_fl-055401975c87952e8_20230121T2105Z_654119f1.txt"), "Unsupported file type.")
		self.assertEqual(self.lambda_module.validateFileType("file.md"), "Unsupported file type.")
		self.assertEqual(self.lambda_module.validateFileType("AWSLogs/841154226728/vpcflowlogs/us-west-2/2023/01/21/841154226728_vpcflowlogs_us-west-2_fl-055401975c87952e8_20230121T2105Z_654119f1.log.gz"), "Valid file type.")
		self.assertEqual(self.lambda_module.validateFileType("841154226728_vpcflowlogs_us-west-2_fl-055401975c87952e8_20230121T2105Z_654119f1.log.gz"), "Valid file type.")
		self.assertEqual(self.lambda_module.validateFileType("841154226728_vpcflowlogs_us-west-2_fl-055401975c87952e8_20230121T2105Z_654119f1.gz"), "Valid file type.")
		self.assertEqual(self.lambda_module.validateFileType("841154226728_vpcflowlogs_us-west-2_fl-055401975c87952e8_20230121T2105Z_654119f1.log.gzip"), "Valid file type.")
		self.assertEqual(self.lambda_module.validateFileType("841154226728_vpcflowlogs_us-west-2_fl-055401975c87952e8_20230121T2105Z_654119f1.gzip"), "Valid file type.")
		self.assertEqual(self.lambda_module.validateFileType("841154226728_vpcflowlogs_us-west-2_fl-055401975c87952e8_20230121T2105Z_654119f1.json"), "Valid file type.")
		self.assertEqual(self.lambda_module.validateFileType("841154226728_vpcflowlogs_us-west-2_fl-055401975c87952e8_20230121T2105Z_654119f1.csv"), "Valid file type.")
		self.assertEqual(self.lambda_module.validateFileType("841154226728_vpcflowlogs_us-west-2_fl-055401975c87952e8_20230121T2105Z_654119f1.log"), "Valid file type.")
		self.assertEqual(self.lambda_module.validateFileType("841154226728_vpcflowlogs_us-west-2_fl-055401975c87952e8_20230121T2105Z_654119f1.parquet"), "Valid file type.")



if __name__ == '__main__':
	unittest.main()