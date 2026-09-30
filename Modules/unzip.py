#packages
import os
import logging
import shutil
import gzip

#defining logger function. We don't have to set it up because its in the main script
logger = logging.getLogger(__name__)

def extract_unzip(data_dir3:str,temp_dir:str):
    """Unzips g zip folders into JSON

    Args:
        data_dir3 (str): The folder you want the JSON to sit in
        temp_dir (str): The folder you're taking the g zip folders from
    """


    #making final folder for unzipped gz files
    os.makedirs(data_dir3, exist_ok=True)

    try:
        # Locate the day folder (assumed to be the numeric folder)
        day_folder = next(f for f in os.listdir(temp_dir) if f.isdigit())
        day_path = os.path.join(temp_dir, day_folder)
    except Exception as e:
        print(f"Error finding day folder: {str(e)}")
        logger.error(f'Error finding day folder: {str(e)}')
        
        raise

    # Walk through the day folder and decompress each .gz file to the data directory
    for root, _, files in os.walk(day_path):
        for file in files:
            if file.endswith('.gz'):
                try:
                    gz_path = os.path.join(root, file)
                    json_filename = file[:-3]  # Remove .gz extension
                    output_path = os.path.join(data_dir3, json_filename)

                    with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file:
                        shutil.copyfileobj(gz_file, out_file)
                    
                    print(f"Successfully processed: {file} -> {json_filename}")
                    logger.info(f"Successfully processed: {file} -> {json_filename}")

                except Exception as e:
                    print(f"Failed to process file {file}: {str(e)}")
                    logger.error(f'Failed to proccess file {file}: {str(e)}')

    try:
        # Delete the temporary directory
        shutil.rmtree(temp_dir)
        print("Temp directory deleted")
        logger.info('Temp directory deleted')

    except Exception as e:
        print(f"Failed to delete temp directory: {str(e)}")
        logger.info(f'Failed to delete temp directory: {str(e)}')
                    
    print(f"All files extracted to the {data_dir3} directory!")
    logger.info(f'All files extracted to the {data_dir3} directory!')