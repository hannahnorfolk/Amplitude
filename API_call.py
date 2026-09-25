#import packages. no JSON package
import requests
from datetime import datetime
import os #because we need to refer to secret file
from dotenv import load_dotenv
load_dotenv()
import zipfile
import gzip
import shutil
import tempfile
import logging



#defining variables
start_time = '20260917T00'
end_time = '20260924T00'
amp_secret_key = os.getenv('AMP_SECRET_KEY')
amp_api_key = os.getenv('AMP_API_KEY')
attempt = 0
max_attempt = 4
url = 'https://analytics.eu.amplitude.com/api/2/export'
params = {
    'start': start_time,
    'end': end_time
}

#making folders to save it in
data_dir = 'data'
os.makedirs(data_dir, exist_ok = True)

#making folder for unzipped data inside the data folder
#data_dir2 = 'data_unzipped'
#  os.makedirs(data_dir2, exist_ok=True)
path_to_zip_file = 'data/data.zip'
directory_to_extract_to = 'data/data.zip'

#making the zip filename
filename = 'data.zip'

#making a timestamp for log files
#Create a timestamp so each extract gets a unique filename
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
log_filename = f'{data_dir}/{timestamp}.json'

#LOGGING
#make a folder for log files 
log_dir = 'log'
os.makedirs(log_dir, exist_ok = True)
log_filename = f'{log_dir}/{timestamp}.json'
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
                    zip_ref.extractall('data/')
     except Exception as e:
            print(f'An error has occurred: {e}')
            logger.error(f'An error has occurred: {e}')
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
        attempt +=1
        print(f'Error code {status}.Trying again. Attempt {attempt} of 3')
        logger.error(f'Error code {status}.Trying again. Attempt {attempt} of 3')
        
