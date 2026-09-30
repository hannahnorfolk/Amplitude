#Packages
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

#Modules
from Modules.log_initialise import setup_logging
from Modules.extract import api_extract
from Modules.unzip import extract_unzip
from Modules.load import load_to_s3

##Logging 
logger = setup_logging('log', timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
logger.info('Logger successfully initialised.')


## API_Extract Parameters
url = 'https://analytics.eu.amplitude.com/api/2/export' #api link
max_attempt = 5
delay = 10
data_dir = 'data' # folder
data_dir2 = 'data_unzipped'
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

#time parameters
current_date = datetime.now()
previous_date = current_date - timedelta(days=3)
start_time = previous_date.strftime('%Y%m%dT%H')
end_time = datetime.now().strftime('%Y%m%dT%H')

#Secret variables
load_dotenv()
AMP_SECRET_KEY=os.getenv('AMP_SECRET_KEY')
AMP_API_KEY=os.getenv('AMP_API_KEY')

## API Extract execution
api_extract(url, data_dir, data_dir2, start_time, end_time, max_attempt, timestamp, delay, AMP_SECRET_KEY, AMP_API_KEY)

## Unzip parameters
data_dir3 = 'data_unzipped_json'
temp_dir = data_dir2

## API Unzip execution
extract_unzip(data_dir3,temp_dir)

## Load variables - the folder is mentioned for the unzip so no need to repeat
AWS_ACCESS_KEY=os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# Load execution
load_to_s3(data_dir3,AWS_ACCESS_KEY,AWS_SECRET_ACCESS_KEY,AWS_BUCKET_NAME)
