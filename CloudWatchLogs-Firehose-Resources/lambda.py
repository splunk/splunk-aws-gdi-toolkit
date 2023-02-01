import os, gzip, json, base64

SPLUNK_SOURCE = os.environ['SPLUNK_SOURCE']
SPLUNK_SOURCETYPE = os.environ['SPLUNK_SOURCETYPE']
SPLUNK_HOST = os.environ['SPLUNK_HOST']
SPLUNK_INDEX = os.environ['SPLUNK_INDEX']

# Default Lambda handler
def handler(event, context):

	returnRecords = []

	# Decode events, and split into separate items in a list
	for record in event['records']:

		# Decode and uncompress raw log event
		decodedData = json.loads(gzip.decompress(base64.b64decode(record['data'])))

		formattedEvents = ""
		returnEvent = {}

		# Loop through each log event, construct event, add to return array
		for logEvent in decodedData['logEvents']:

			# Format Splunk event
			formattedEvents += '{ "time": ' +  str(logEvent['timestamp']) + ', "host": "' + SPLUNK_HOST + '", "source": "' + SPLUNK_SOURCE + '", "sourcetype": "' + SPLUNK_SOURCETYPE + '", "index": "' + SPLUNK_INDEX + '", "event": "' + " ".join(str(logEvent['message']).split()) + '"}'
		
		# Construct return event
		returnEvent['recordId'] = dict(record)['recordId']
		returnEvent['result'] = "Ok"
		returnEvent['data'] = base64.b64encode(formattedEvents.encode('utf-8')).decode()

		# Print for debugging
		print("Processed record " + record['recordId'])

		# Add return events to array to return all the records to Firehose
		returnRecords.append(returnEvent)

	return {'records': returnRecords}
