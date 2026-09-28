# Amplitude

Python project extracting data from the amplitude API

## Ingestion

There are 2 key python files: Extract_API.py and Extract_Unzip.py
I have tried to separate these into logical sections

### 1) API_call

Section 1: Importing packages
Here I import the relevant packages needed for the script

Section 2: Load dotenv
This is needed to refer to the secret passwords

Section 3: Defining variables
Here I define everything I need for the API call. These include: api keys, attempts, start/end date, url

Section 4: Making folders
Here I make 3 folders: one for my zip, one for my unzip, and one for my .json files

Section 5: Logging
Here I set up a logging file.

Section 6: The API Call
My API call is firstly wrapped in a loop so I can have up to 3 attempts.

I then make the API call, and the status output of these are wrapped in a large if statement to accommodate for different statuses.

In summary:

If status = 200, then I proceed to saving the files.
If status = 400, 404, I then return the status code and no more attempts are made.
If there is another error code, wait 10s and try again.

If the status = 200:
Save the .zip in a folder.

### 2) Unzip file

Similarly to the API call file, this file imports relevant packages and lists relevant variables.
This file passes through each .gz folder in the file and saves it to another folder.

## Load

There is one python file titled Load.py. In summary, this pulls the unzipped .json files from the folder data_unzipped_json and this puts this into the S3 bucket made in AWS.
A breakdown of this file is as follows:

Section 1: Importing packages
Here I import the relevant packages needed for the script

Section 2: Load dotenv
This is needed to refer to the passwords stored on my .env .
The passwords needed for this sections are my Access Key and Access Secret linked to a specific user created on AWS.

Section 3: Setting Up logging
Similar to my other python files, I set up a logging file prefixed 'load\_' to record key details and/or errors.

Section 4: Obtaining user authentication from the .env
Here I get my AWS Access Key and Access Secret linked to a specific user I created for this project on AWS. I also detail the S3 bucket name I created.

Section 5: Create a connection to the AWS user
Uses boto3.client to specify client information

Section 6: File migration to the S3 bucket. Here a for loop is made to pass through each file in my unzipped folder to move it to the s3 bucket. Once this is done, the file is removed.
Error handling is also managed in this section
