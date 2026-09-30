# Amplitude Data Extraction and AWS S3 Pipeline

A Python-based data pipeline that extracts event data from the Amplitude Export API, decompresses the returned files, and uploads the resulting JSON files to an AWS S3 bucket.

## Description

This project automates the extraction and loading of data from the Amplitude Export API into an AWS S3 bucket. The pipeline consists of three Python scripts that perform separate stages of the process.

The first script connects to the Amplitude Export API and requests data for the previous three days. The API response is saved as a timestamped ZIP file and then extracted into a temporary directory. API responses are handled using status codes, with retry functionality for unsuccessful requests. Logging is also used to record the progress and any errors encountered during the extraction.

The second script processes the extracted files. Amplitude returns the event data as compressed .gz files, so this script locates the extracted files, decompresses them, and saves the resulting JSON files into a separate directory. Once processing is complete, the temporary extracted directory is deleted.

The third script connects to AWS using boto3 and uploads each JSON file to a specified Amazon S3 bucket. After a file has been successfully uploaded, the local copy is deleted.

The overall pipeline is therefore:

Amplitude API → ZIP file → extracted .gz files → JSON files → AWS S3

### Getting Started

### Dependencies

The following are required to run this project:

- Python 3.12
- An Amplitude account with access to the Export API
- An Amplitude API key and secret key
- An AWS account
- An AWS S3 bucket
- AWS access credentials with permission to upload files to the bucket

To see what packages are required, please execute:

```
pip install -r requirements.txt
```

### .env variables required

AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_BUCKET_NAME=your_s3_bucket_name

AMP_API_KEY
AMP
AMP_DATA_REGION

### Project folders

The scripts automatically create the folders they require.

After running the pipeline, the project will create 3 folders:

- Data = this contains the unzipped file
- Data_Unzipped = contains the unzipped .gz files
- Data_unzipped_json = contains the final .json files ready for movement into the S3 bucket

## Executing program

The scripts should be run in the following order.

1. Extract_API.py
2. Extract_Unzipped.py
3. Load.py

## Authors

Hannah Norfolk

This project is currently not licensed. If this repository is intended to be shared publicly, consider adding an appropriate open-source license.

## Licence

This project is licenced under MIT licence.
