#import packages.
import requests
from datetime import datetime, timedelta
import os #because we need to refer to secret file
from dotenv import load_dotenv
import logging
import time
import zipfile

#Load dotenv() --> what does this mean?
load_dotenv()

#DEFINING VARIABLES
#authentication
amp_secret_key = os.getenv('AMP_SECRET_KEY')
amp_api_key = os.getenv('AMP_API_KEY')

#attempts
attempt = 0
max_attempt = 4
delay = 10

#time parameters
current_date = datetime.now()
previous_date = current_date - timedelta(days=3)

start_time = previous_date.strftime('%Y%m%dT%H')
end_time = datetime.now().strftime('%Y%m%dT%H')

params = {
    'start': start_time,
    'end': end_time
}
url = 'https://analytics.eu.amplitude.com/api/2/export'


#making folder to save it in
data_dir = 'data'
os.makedirs(data_dir, exist_ok = True)

#making folder for unzipped data inside the data folder
data_dir2 = 'data_unzipped'
os.makedirs(data_dir2, exist_ok=True)

#making final folder for unzipped gz files
data_dir3 = 'data_unzipped_json'
os.makedirs(data_dir3, exist_ok=True)

#making the zipped file
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
filename = f'{data_dir}/{timestamp}.zip'
path_to_zip_file = f'{filename}'
directory_to_extract_to = f'{filename}'

#making a timestamp for log files
#Create a timestamp so each extract gets a unique filename
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
log_filename = f'{data_dir}/{timestamp}.log'

#LOGGING
#make a folder for log files 
log_dir = 'log'
os.makedirs(log_dir, exist_ok = True)
log_filename = f'{log_dir}/{timestamp}.log'

# Configure logging so messages are written to the log file
logging.basicConfig(
    filename=log_filename,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level= logging.INFO
)

#Making a logger and confirming it has been set up
logger = logging.getLogger()
logger.info('Logger successfully initialised')

#Keep trying until max attempts are reached
while attempt < max_attempt:
    
    #doing the API request
    response = requests.get(url, params=params, auth=(amp_api_key,amp_secret_key))
    status = response.status_code
    status_text = response.text

    #IF STATEMENTS BASED ON STATUS CODES

    ##if its a success:
    if status ==200:
     print(f'API Status {status}')

     try:
          with open(path_to_zip_file,'wb') as file:
                file.write(response.content)
                print(f'{filename} was successfully saved. Yipee!')
                logger.info(f'{filename} was successfully saved. Yipee!')

             #time to unzip
          with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
             zip_ref.extractall(data_dir2)
             print(f'File was successfully unzipped')
             logger.info(f'File was successfully unzipped')

     except Exception as e:
            print(f'An error has occurred: {e}')
            logger.error(f'An error has occurred: {e}')

    #time to unzip again
    #with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file:
     #  shutil.copyfileobj(gz_file, out_file)

        #making the gz files - we need the filepath, filename and location of where to put it
      #  gz_path = os.path.join(data_dir2,filename)
       # json_filename = f'{filename}.json.gz'[:3]
       # output_path = os.path.join(data_dir, json_filename)

     break

    #if the api call didn't work
    elif status ==400:
        status_text = response.text
        print(f'Error code {status}.The file size of the exported data is too large. Shorten the time ranges and try again. The limit size is 4GB.')
        logger.error(f'Error code {status}.The file size of the exported data is too large. Shorten the time ranges and try again. The limit size is 4GB.')
        break

    elif status ==404:
         status_text = response.text
         print(f'Error code {status}. No data available for the time range requested.')
         logger.info(f'Error code {status}. No data available for the time range requested.')
         break
    
    else:
        time.sleep(delay)
        attempt +=1
        print(f'Error code {status}.Trying again. Attempt {attempt} of {max_attempt}')
        logger.error(f'Error code {status}.Trying again. Attempt {attempt} of {max_attempt}')
        
