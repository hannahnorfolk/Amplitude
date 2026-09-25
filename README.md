# Amplitude

Python project extracting data from the amplitude API

There are 2 key python files: API_call.py and unzip.py
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
