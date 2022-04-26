# Splunk AWS GDI Tookit

This repo is for individuals and organizations looking to get better visibility, observability, and monitoring in their AWS account or AWS accounts.  There are sets of CloudFormation templates here designed to help get data related to AWS accounts and services to Splunk for analysis and alerting.


## Single AWS Account Monitoring
Single account monitoring is designed to use the [Splunk Data Manager](https://docs.splunk.com/Documentation/DM/latest/User/About) to send the data to [Splunk Cloud](https://www.splunk.com/en_us/software/splunk-cloud-platform.html).  The Splunk Data Manager will provide CloudFormation templates to configure AWS-based resources to send data to Splunk Cloud.

Monitoring a single AWS account consists of two primary steps:
1. Deploy the CloudFormation templates in the Single Account CloudFormation directory to enable services
2. Configure Splunk Cloud to receive the data
3. Configure the Splunk Data Manager to send the data to Splunk


### 1. Deploying the Single Account CloudFormation Templates
The CloudFormation templates need to be deployed to the AWS account to enable services that you want to retrieve data from.  There are 4 CloudFormation templates in the Single Account CloudFormation directory, 1 for each service that needs to be enabled.

- cloudTrail.yml: This CloudFormation template is used to enable [CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html) logging to CloudWatch logs, and an S3 bucket that is created as part of the CloudFormation template.  Some parameters can be set during the deployment of the template:
	- cloudTrailLogFileValidation: Used to enable or disable [CloudTrail File Validation](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-intro.html).
	- cloudTrailIncludeGlobalServiceEvents: Used to enable or disable logging of [CloudTrail global service events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html#cloudtrail-concepts-global-service-events).
	- cloudTrailMultiRegionLogging: Used to enable or disable logging of CloudTrail logs from all regions.  The default is `true`, which means that the CloudTrail will be created and log activity from all regions.  If you want to only log from specific regions, set this to `false`, and deploy this CloudFormation template to each region individually that you want to monitor.
- guardDuty.yml: This template is used to enable [Amazon GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html) in an individual region.  This template needs to be deployed to each region individually that will be monitored with GuardDuty.
- iamAccessAnalyzer.yml: This template enables [AWS IAM Access Analyer](https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html).  Like Amazon GuardDuty, AWS IAM Access Analyzer is enabled on a pre-region basis and therefore this CloudFormation template needs to be deployed to each region you want to monitor.
- securityHub.yml:  This template enables [AWS Security Hub](https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html).  AWS Security Hub also needs to be enabled in each region you want to monitor.

The easiest way to deploy these CloudFormation templates is via the [AWS CloudFormation Console](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html).



### 2. Configure Splunk Cloud to Receive the Data
The only configuration that needs to be done Splunk-side in this step is [adding any indexes](https://docs.splunk.com/Documentation/SplunkCloud/latest/Admin/ManageIndexes) that are needed to receive the data.  You may want to create an index for all of the AWS-related data (eg a single index named `aws`), or split out the data by use-case (eg CloudTrail data would go to an index named `aws`, but AWS RDS logs would go to an index named `database`).  If you're setting this up just to see what data will look like, we recommend creating an `aws` index for this data.


### 3. Configure Splunk Data Manager
Follow the instructions in the [Data Manager documentation for onboarding data from a single account](https://docs.splunk.com/Documentation/DM/1.4.0/User/AWSSingleAccount).
