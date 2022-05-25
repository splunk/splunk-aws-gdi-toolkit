import boto3, gzip, json, os, sys, shutil, tarfile

# AWS-related setup
s3Client = boto3.client('s3')
firehoseDeliverySreamName = os.environ['firehoseDeliverySreamName']
firehoseClient = boto3.client('firehose', region_name=os.environ['AWS_REGION'])

# Splunk-related setup
SPLUNK_INDEX = boto3.client('firehose', region_name=os.environ['SPLUNK_INDEX'])
SPLUNK_TIME = boto3.client('firehose', region_name=os.environ['SPLUNK_TIME'])
SPLUNK_SOURCETYPE = boto3.client('firehose', region_name=os.environ['SPLUNK_SOURCETYPE'])
SPLUNK_SOURCE = boto3.client('firehose', region_name=os.environ['SPLUNK_SOURCE'])
SPLUNK_HOST = boto3.client('firehose', region_name=os.environ['SPLUNK_HOST'])
SPLUNK_JSON_KEY = boto3.client('firehose', region_name=os.environ['SPLUNK_JSON_KEY'])
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

			return(path)

	except:
		return("Unable to uncompress file")

	return(path)


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

		# Send object info to be uncompressed
		uncompressResult = uncompressFile(downloadResult)

		# If the file was unable to be compressed, print the error and stop this loop
		if ("Unable to uncompress file" in uncompressResult):
			print("Unable to uncompress file s3://" + objectInfo["bucket"] + "/" + objectInfo["key"])
			continue
