#import
import logging
import zipfile
import os
import requests
import time

#defining logger function. We don't have to set it up because its in the main script
logger = logging.getLogger(__name__)

def api_extract(url:str, data_dir:str, data_dir2:str, start_time:str, end_time:str, max_attempt:str, timestamp:str, delay:str, AMP_SECRET_KEY:str, AMP_API_KEY:str):
    """Extracts a zip folder from the specified URL and saves it locally in the data_dir. This gets unzipped into a list of .gzip files and saves locally in data_dir2.

    Args:
        url (str): The URL you want to download 
        data_dir (str): The folder you want the initial ZIP to be saved to
        data_dir2 (str): The folder you want the g zips to be saved to
        start_time (str): The start time of the data
        end_time (str): The end time of the data
        max_attempt (str): Maximum number of attempts to call the API if there is an error
        timestamp (str): What the initial ZIP file will be named
        delay (str): Duration in seconds to wait between API call attempts
        AMP_SECRET_KEY (str): Amplitude API secret key
        AMP_API_KEY (str): Amplitude API key
    """

    #attempts
    attempt = 0

    params = {
        'start': start_time,
        'end': end_time
    }

    #making folder to save it in
    os.makedirs(data_dir, exist_ok = True)

    #making folder for unzipped data inside the data folder
    os.makedirs(data_dir2, exist_ok=True)

    #making the zipped file
    filename = f'{data_dir}/{timestamp}.zip'
    path_to_zip_file = f'{filename}'
    directory_to_extract_to = f'{filename}'

    #Keep trying until max attempts are reached
    while attempt < max_attempt:
        
        #doing the API request
        response = requests.get(url, params=params, auth=(AMP_API_KEY,AMP_SECRET_KEY))
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
            
