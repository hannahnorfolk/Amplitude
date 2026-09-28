#import packages. no JSON package
import requests
from datetime import datetime, timedelta
import os #because we need to refer to secret file
from dotenv import load_dotenv
import zipfile
import gzip
import shutil
import tempfile
import logging
import json
import time

#variables

temp_dir = 'data_unzipped'
data_dir = 'data_unzipped_json'



try:
    # Locate the day folder (assumed to be the numeric folder)
    day_folder = next(f for f in os.listdir(temp_dir) if f.isdigit())
    day_path = os.path.join(temp_dir, day_folder)
except Exception as e:
    print(f"Error finding day folder: {str(e)}")
    raise

# Walk through the day folder and decompress each .gz file to the data directory
for root, _, files in os.walk(day_path):
    for file in files:
        if file.endswith('.gz'):
            try:
                gz_path = os.path.join(root, file)
                json_filename = file[:-3]  # Remove .gz extension
                output_path = os.path.join(data_dir, json_filename)

                with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file:
                    shutil.copyfileobj(gz_file, out_file)
                
                print(f"Successfully processed: {file} -> {json_filename}")
            except Exception as e:
               print(f"Failed to process file {file}: {str(e)}")

try:
    # Delete the temporary directory
    shutil.rmtree(temp_dir)
    print("Temp directory deleted")

except Exception as e:
    print(f"Failed to delete temp directory: {str(e)}")

print("All files extracted to the 'data' directory!")