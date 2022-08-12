import json, os, base64, datetime, copy

SPLUNK_EVENT_TYPE = os.environ['SPLUNK_EVENT_TYPE']
SPLUNK_SOURCE = os.environ['SPLUNK_SOURCE']
SPLUNK_HOST = os.environ['SPLUNK_HOST']
SPLUNK_INDEX = os.environ['SPLUNK_INDEX']


def parseEventAsEvent(message):

	# Parse as JSON event
	jsonMessage = json.loads(message)

	# Create Splunk Event
	splunkEvent = {}
	splunkEvent["Average"] = jsonMessage['value']['sum'] / jsonMessage['value']['count']
	splunkEvent["Maximum"] = jsonMessage['value']['max']
	splunkEvent["Minimum"] = jsonMessage['value']['min']
	splunkEvent["SampleCount"] = jsonMessage['value']['count']
	splunkEvent["Sum"] = jsonMessage['value']['sum']
	splunkEvent["Unit"] = jsonMessage['unit']
	splunkEvent["account_id"] = jsonMessage['account_id']
	splunkEvent["metric_name"] = jsonMessage['metric_name']
	splunkEvent["Namespace"] = jsonMessage['namespace']
	splunkEvent["timestamp"] = datetime.datetime.fromtimestamp(jsonMessage['timestamp']/1000).isoformat() + "Z"
	metric_dimensions = ""
	for dimensionKey in jsonMessage['dimensions'].keys():
		metric_dimensions += (str(dimensionKey) + "=[" + str(jsonMessage['dimensions'][str(dimensionKey)]) + "],")
	splunkEvent["metric_dimensions"] = metric_dimensions[:-1]

	# Return Splunk event
	return '{ "time": ' +  str(jsonMessage['timestamp']) + ', "host": "' + SPLUNK_HOST + '", "source": "' + SPLUNK_SOURCE + '", "sourcetype": "aws:cloudwatch", "index": "' + SPLUNK_INDEX + '", "event": ' + json.dumps(splunkEvent) + ' }'


def parseEventAsMetric(message):

	# Parse as JSON event
	jsonMessage = json.loads(message)

	# Create Splunk Event
	splunkEvent = {}
	splunkEvent["AccountID"] = jsonMessage['account_id']
	splunkEvent["MetricName"] = jsonMessage['metric_name']
	splunkEvent["Namespace"] = jsonMessage['namespace']
	splunkEvent["Unit"] = jsonMessage['unit']
	splunkEvent["Region"] = jsonMessage['region']
	splunkEvent["metric_name:" + jsonMessage['namespace'] + "." + jsonMessage['metric_name'] + ".Average"] = jsonMessage['value']['sum'] / jsonMessage['value']['count']
	splunkEvent["metric_name:" + jsonMessage['namespace'] + "." + jsonMessage['metric_name'] + ".Maximum"] = jsonMessage['value']['max']
	splunkEvent["metric_name:" + jsonMessage['namespace'] + "." + jsonMessage['metric_name'] + ".Minimum"] = jsonMessage['value']['min']
	splunkEvent["metric_name:" + jsonMessage['namespace'] + "." + jsonMessage['metric_name'] + ".SampleCount"] = jsonMessage['value']['count']
	splunkEvent["metric_name:" + jsonMessage['namespace'] + "." + jsonMessage['metric_name'] + ".Sum"] = jsonMessage['value']['sum']
	for dimensionKey in jsonMessage['dimensions'].keys():
		splunkEvent[dimensionKey] = jsonMessage['dimensions'][str(dimensionKey)]

	# Return Splunk event
	return '{ "time": ' +  str(jsonMessage['timestamp']) + ', "host": "' + SPLUNK_HOST + '", "source": "' + SPLUNK_SOURCE + '", "sourcetype": "aws:cloudwatch:metric", "index": "' + SPLUNK_INDEX + '", "event": "metric",  "fields": ' + json.dumps(splunkEvent) + ' }'

# Default Lambda handler
def handler(event, context):

	returnRecords = []

	# Decode events, and split into separate items in a list
	for record in event['records']:

		data = base64.b64decode(record['data']).decode('utf-8').splitlines()

		formattedEvents = ""
		returnEvent = {}

		for message in data:

			# Parse event as event-style message
			if (SPLUNK_EVENT_TYPE == "event"):
				formattedEvents += parseEventAsEvent(message) + "\n"

			# Parse event as metric-style message
			elif (SPLUNK_EVENT_TYPE == "metric"):
				formattedEvents += parseEventAsMetric(message) + "\n"

		print(formattedEvents)

		returnEvent['recordId'] = dict(record)['recordId']
		returnEvent['result'] = "Ok"
		returnEvent['data'] = base64.b64encode(bytearray(formattedEvents, 'utf-8'))

		returnRecords.append(returnEvent)

	return {'records': returnRecords}
