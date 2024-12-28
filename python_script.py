'''
python_script.py

Runs all requested processing on the provided Excel file for the PracticePanther Data Migrations test.
I've included comments to highlight code functionality as well as potential areas for refinement.

Author: Ryne Smith
Last Modified: 12/27/2024
'''
import pandas as pd
import dateutil
import datetime

#read in data using standard pandas xlsx parsing function
data = pd.read_excel('Migration_Interview_Data (Python).xlsx')
print('Loaded input data. Processing...\n')

#remove any duplicate rows from the data
#by default, checks duplicates using every column
#we can pass an argument to the function to specify columns to check if needed, i.e. ID column only
data = data.drop_duplicates()

#append "Contact: " to all column names
data = data.rename(mapper=lambda x: 'Contact: '+x, axis=1)

#modify all name fields to use capitalized first character followed by lowercase remaining characters
#this can throw an error on names with length 1. We can add an if/else to account for this if needed.
def nameCaseMapper (orig_name):
    return orig_name[0].upper() + orig_name[1:].lower()
data['Contact: First Name'] = data['Contact: First Name'].apply(nameCaseMapper)
data['Contact: Middle Name'] = data['Contact: Middle Name'].apply(nameCaseMapper)
data['Contact: Last Name'] = data['Contact: Last Name'].apply(nameCaseMapper)

#modify birth date field to map into common MM/DD/YYYY format
#errors possible on original data formats that cannot be parsed into datetime object
#try catch can solve this but will require some manual work for unrecognized formats
def dateMapper(orig_date):
    #some rows may be automatically converted to datetime objects by pandas
    if not isinstance(orig_date, datetime.datetime):
        orig_date = dateutil.parser.parse(orig_date)
    return orig_date.strftime("%m/%d/%Y")
data['Contact: Date of Birth'] = data['Contact: Date of Birth'].apply(dateMapper)

#generate unique IDs for each unique record
#if inserting into existing database, will need to check these ids for uniqueness against existing data
data['Contact: ID'] = data.index+1

#map specific assignment column values to new ones
#uses default for any missing values
def assignedMapper(orig_assigned):
    if orig_assigned == 'AA':
        return 'Aaron Artsen'
    elif orig_assigned == 'BL':
        return 'Bond Liver'
    elif orig_assigned == 'IC':
        return 'Individual Contributor'
    elif orig_assigned == 'TM':
        return 'Tim Mint'
    else:
        return 'Gabe Michel'

data['Contact: Assigned'] = data['Contact: Assigned'].apply(assignedMapper)

#perform simple automated verifications of processed data
#these are basic examples but more refined tests can be added
print('Processing complete. Running verifications on output data:\n')
#verify no duplicate entire rows
if data.duplicated().value_counts().tolist()[0] != data.shape[0]:
    print('\t[WARNING] Duplicate rows detected. Double check output file for duplications.\n')
else:
    print('\t[PASS] No duplicated rows detected in output.\n')

#verify no repeated IDs
if data['Contact: ID'].nunique() != data.shape[0]:
    print('\t[WARNING] Duplicate record IDs detected. Double check output file for duplicated ID values.\n')
else:
    print('\t[PASS] No duplicated record IDs detected in output.\n')

#verify no missing values
if data.isna().sum().sum() > 0:
    print('\t[WARNING] Missing values detected in output data. Double check output file for missing values.\n')
else:
    print('\t[PASS] No missing values detected in output data.\n')

#output processed data in CSV format
data.to_csv('output_data.csv', index=False)
print('Verifications complete. Output data saved to output_data.csv')