import boto3, gzip, json, os, sys

s3Client = boto3.client('s3')
firehoseDeliverySreamName = os.environ['firehoseDeliverySreamName']
firehoseClient = boto3.client('firehose', region_name=os.environ['AWS_REGION'])

def retrieveS3Object(record):

	try:
		# Set bucket and key to retrieve
		record = json.loads(record['body'])
		bucket = record['Records'][0]['s3']['bucket']['name']
		key = record['Records'][0]['s3']['object']['key']

	except:
		return("SQS message did not contain S3 file information.  Record: " + str(record))

	try:
		# Download VPC Flow Log file from S3
		s3Client.download_file(bucket, key, "/tmp/" + key.split("/")[-1] + ".gz")
	except:
		return("Unable to download file s3://" + bucket + "/" + key)

	return("Downloaded VPC Flow Log file s3://" + bucket + "/" + key)


def processVPCFlowLogFile(record):

	# Set bucket and key to retrieve
	record = json.loads(record['body'])
	bucket = record['Records'][0]['s3']['bucket']['name']
	key = record['Records'][0]['s3']['object']['key']

	try:
		with gzip.open("/tmp/" + key.split("/")[-1] + ".gz", "rb") as f:
			data = f.read().decode("ascii")

	except:
		return("Unable to decode file s3://" + bucket + "/" + key)

	
	# Parse VPC Flow Log data
	try:
		vpcFlowLogs = data.split("\n")[1:-1] #0 will always be the CSV headers, and -1 will always be empty, so drop both of those.
	except:
		return("Unable to parse VPC Flow Log records from s3://" + bucket + "/" + key)


	# Send data to Firehose
	try:

		recordBatch = []

		for vpcFlowLog in vpcFlowLogs:
			# Add record to recordbatch
			recordBatch.append({"Data": vpcFlowLog + "\r\n"})

			# If there are more than 250 records or 2MB in the sending queue, send the event to Splunk and clear the queue
			if (len(recordBatch) > 250 or (sys.getsizeof(recordBatch) > 2000000 )):
				firehoseClient.put_record_batch(DeliveryStreamName=firehoseDeliverySreamName, Records=recordBatch)
				recordBatch.clear()

		# Send any remaining records to Splunk
		if (len(recordBatch) > 0):
			firehoseClient.put_record_batch(DeliveryStreamName=firehoseDeliverySreamName, Records=recordBatch)
			recordBatch.clear()

	except:
		return("Unable to send record to Firehose s3://" + bucket + "/" + key)


	return("Processed VPC Flow Log records from s3://" + bucket + "/" + key)


def handler(event, context):

	for record in event['Records']:

		# Parse SQS message and download file from S3
		retrievalResult = retrieveS3Object(record)
		print(retrievalResult)		

		# Process file, only if it was successfully downloaded
		if ("Downloaded VPC Flow Log file" in retrievalResult):
			processResult = processVPCFlowLogFile(record)
			print(processResult)