# Import necessary packages
import os
import boto3
from dotenv import load_dotenv
import logging
from datetime import datetime

#load_dotenv stuff to activate .env
load_dotenv()

#Setting up logging

#Create a timestamp so each extract gets a unique filename
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
#Create a folder for log files if it doesn't already exist
log_dir = 'log'
os.makedirs(log_dir, exist_ok = True)
log_filename = f'{log_dir}/load_{timestamp}.log'

# Configure logging so messages are written to the log file
logging.basicConfig(
    filename=log_filename,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level= logging.INFO
)

# Create the logger and confirm that it has been successfully set up
logger = logging.getLogger()
logger.info('Logger successfully initialised')


# Grab user authentication details from the.env file
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')


# Create a connection to the AWS User
s3_client = boto3.client(
    's3',
    aws_access_key_id = AWS_ACCESS_KEY, #have to write in this format as this is an optional field
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY # also optional field, see above
)

# Establish a list of all the files that we wish to upload
files_to_upload = os.listdir('data_unzipped_json')


# Create a loop to go through each file
for file in files_to_upload:
    file_to_upload = f'data_unzipped_json/{file}' #one file we extracted that we would like to upload to s3
    try:
        #file_to_upload = the file we extracted that we would like to upload to s3
        #file = what we want the file to appear as in s3
        #files_to_upload = all the files we extracted that we want to uplod to s3

        # Link the user details, files, and S3 bucket together
        s3_client.upload_file(file_to_upload,AWS_BUCKET_NAME,file)

        print(f'{file} has uploaded successfully.')
        logger.info(f'{file} has uploaded successfully.')
        os.remove(file_to_upload)
    except Exception as e:
        print(f'An error has occurred. {e}')
        logger.error(f'An error has occurred. {e}')

