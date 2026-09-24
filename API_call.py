#import packages. no JSON package
import requests
from datetime import datetime
import os #because we need to refer to secret file
from dotenv import load_dotenv
load_dotenv()


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

#Create a timestamp so each extract gets a unique filename
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
filename = f'{data_dir}/{timestamp}.zip'

#Keep trying until max attempts are reached

while attempt < max_attempt:
    
    #doing the API request
    response = requests.get(url, params=params, auth=(amp_api_key,amp_secret_key))

    #print the status code
    status = response.status_code
    print(response.status_code)

    #IF STATEMENTS BASED ON STATUS CODES. 'wb' needed for ZIP files, 'w' was json
    if 200<=status<300:
     with open(filename, 'wb') as file:
        file.write(response.content)
     break
    else:
        print('Something is srsly wrong.')
        attempt+=1