import boto3, gzip, json, os, sys, shutil, re, dateutil.parser, time

# AWS-related setup
s3Client = boto3.client('s3')
firehoseDeliverySreamName = os.environ['firehoseDeliverySreamName']
firehoseClient = boto3.client('firehose', region_name=os.environ['AWS_REGION'])
recordBatch = []

# Splunk-related setup
SPLUNK_INDEX = boto3.client('firehose', region_name=os.environ['SPLUNK_INDEX'])
SPLUNK_TIME_PREFIX = boto3.client('firehose', region_name=os.environ['SPLUNK_TIME_PREFIX'])
SPLUNK_TIME_FORMAT = boto3.client('firehose', region_name=os.environ['SPLUNK_TIME_FORMAT'])
SPLUNK_SOURCETYPE = boto3.client('firehose', region_name=os.environ['SPLUNK_SOURCETYPE'])
SPLUNK_SOURCE = boto3.client('firehose', region_name=os.environ['SPLUNK_SOURCE'])
SPLUNK_HOST = boto3.client('firehose', region_name=os.environ['SPLUNK_HOST'])
SPLUNK_JSON_FORMAT = boto3.client('firehose', region_name=os.environ['SPLUNK_JSON_FORMAT'])
SPLUNK_CSV_IGNORE_FIRST_LINE = boto3.client('firehose', region_name=os.environ['SPLUNK_CSV_IGNORE_FIRST_LINE'])


# Parse SQS message for bucket information
def retrieveObjectInfo(record):
	
	# Try to parse the record for file information
	try:
		record = json.loads(record['body'])
		bucket = record['Records'][0]['s3']['bucket']['name']
		key = record['Records'][0]['s3']['object']['key']

		# Construct and return the result
		result = {}
		result["bucket"] = bucket
		result["key"] = key
		return result

	# Return an error if the record doesn't have a valid file defined in it
	except:
		return("SQS message did not contain S3 file information.  Record: " + str(record))


# Retrieve the S3 object, and return the new path
def downloadS3Object(bucket, key):

	try:
		# Define the path for the file
		path = "/tmp/" + key.split("/")[-1]

		# Download the file from the S3 bucket
		s3Client.download_file(bucket, key, path)

		# Return the new file path
		return(path)

	except:
		return("Unable to download file s3://" + bucket + "/" + key)


# Uncompress the file if it needs to be uncompressed, then return the path and the new file extension
def uncompressFile(path):

	# Set file extension and new file path (if it gets uncompressed)
	extension = path.split(".")[-1]
	uncompressedFilePath = path[0:(-1*(len(extension)) - 1)]

	try:
		# If gzip file...
		if (extension == "gz" or extension == "gzip"):

			# Uncompress file
			with gzip.open(path, 'rb') as f_in:
				with open(uncompressedFilePath, 'wb') as f_out:
					shutil.copyfileobj(f_in, f_out)

			# Remove the uncompressed file
			os.remove(uncompressedFilePath)

			return(path)

	except:
		return("Unable to uncompress file")

	return(path)


# Split events into a list. Additional file extensions should be added here.
def splitEvents(events, extension):

	if (extension == "csv" or extension == "log"):
		splitEvents = events.split("\n")
		events.clear()

	elif (extension == "json"):
		if (SPLUNK_JSON_FORMAT == "eventsInRecords"):
			splitEvents = json.loads(events)["Records"]
			events.clear()


# Set timestamp on event
def getTimestamp(event):

	# For ISO8601 (%Y-%m-%dT%H-%M-%S.%fZ)
	if (SPLUNK_TIME_FORMAT = "ISO8601"):
		iso8601Timestamp = re.search("" + SPLUNK_TIME_PREFIX + ".{1,5}(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)", str(splitEvent)).group(1) #fix eventTime
		return(dateutil.parser.parse(iso8601Timestamp).timestamp())
	# If not standard, set to current time
	else:
		return(time.time())

# Buffer and send events to Firehose
def sendEventsToFirehose(event, final):

	# Add current event ot recordBatch
	if (len(event) > 0): # This will be 0 if it's a final call to clear the buffer
		recordBatch.append({"Data": event})

	try:

		# If there are more than 200 records or 2MB in the sending queue, send the event to Splunk and clear the queue
		if (len(recordBatch) > 200 or (sys.getsizeof(recordBatch) > 2000000 )):
			firehoseClient.put_record_batch(DeliveryStreamName=firehoseDeliverySreamName, Records=recordBatch)
			recordBatch.clear()
		elif (final == True):
			firehoseClient.put_record_batch(DeliveryStreamName=firehoseDeliverySreamName, Records=recordBatch)
			recordBatch.clear()
	except:
		return("Unable to send file to Firehose")

	return("Sent to Firehose")


# Default Lambda handler
def handler(event, context):

	# Loop through each SQS message
	for message in event['Records']:

		# Retrieve bucket name and key from SQS message
		objectInfo = retrieveObjectInfo(record)

		# If a string was returned instead of a dictionary, print the error and stop this loop
		if (isinstance(objectInfo, str)):
			print(objectInfo)
			continue
		
		# Retrieve the S3 object and uncompress it
		downloadResult = downloadS3Object(objectInfo["bucket"], objectInfo["key"])
		
		# If the file was unable to be downloaded, print the error and stop this loop
		if ("Unable to download" in downloadResult):
			print(downloadResult)
			continue

		# Send file info to be uncompressed
		uncompressResult = uncompressFile(downloadResult)

		# If the file was unable to be compressed, print the error and stop this loop
		if ("Unable to uncompress file" in uncompressResult):
			print("Unable to uncompress file s3://" + objectInfo["bucket"] + "/" + objectInfo["key"])
			continue

		# Try to read the file contents into memory
		try:
			with open(path, 'r') as f:
				events = f.read()
		except:
			print("Unable to read file contents into memory")
			continue

		# Set extension 
		extension = path.split(".")[-1]

		# Split events
		splitEvents = splitEvents(events, extension)

		# Loop through split events
		for splitEvent in splitEvents:

			# Get timetamp
			timestamp = getTimestamp(event)

			# Construct event to send to Splunk
			event = { "time": timestamp, "host": SPLUNK_HOST, "source": SPLUNK_SOURCE, "sourcetype": SPLUNK_SOURCETYPE, "index": SPLUNK_INDEX, "event":  splitEvent }

			# Buffer and send the evnets to Firehose
			result = sendEventsToFirehose(str(event), False)

			# Error logging
			if (result == "Unable to send to Firehose"):
				print("Unable to send to Firehose: " + firehoseDeliverySreamName)

		# Send the remaining events to Firehose, effectively clearing the buffered events in recordBatch
		sendEventsToFirehose("", True)

		# Delete the file to clear up space in /tmp to make room for the next one
		os.remove(path)

		# Logging
		print("Processed file s3://" + objectInfo["bucket"] + "/" + objectInfo["key"])

