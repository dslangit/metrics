#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np 
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# # Functions

# In[2]:


def initiate(json_cred, url):
    '''
    This function is for opening the connection to the GSheet.
    Inputs: JSON credential file, URL of the Gsheet.
    '''
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_cred, scope)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_url(url)
    return spreadsheet


# In[3]:


def unique_user(spreadsheet, csv_unique_user, num_sheet):
    '''
    This function is for appending the new rows on the existing unique_user sheet.
    Inputs: CSV of the unique user, numerical sequence of the sheet.
    Numerical sequence of the sheet is +1 because Python starts at 0.
    '''
    df = pd.read_csv(csv_unique_user).transpose().reset_index()
    df = df.iloc[1:]
    worksheet = spreadsheet.get_worksheet(num_sheet)
    worksheet.append_rows(df.values.tolist())
    # Display
    user_table = spreadsheet.get_worksheet(num_sheet).get_all_records()
    user_table_df = pd.DataFrame.from_dict(user_table)


# In[4]:


def source(spreadsheet, csv_source, num_sheet):
    '''
    This function is for appending the new rows on the existing split by source sheet.
    Inputs: CSV of the split by source, numerical sequence of the sheet.
    Numerical sequence of the sheet is +1 because Python starts at 0.
    Hard-coded cell-range, need to update this if the Gsheet range is changed.
    '''
    worksheet = spreadsheet.get_worksheet(num_sheet+1)
    cell_range = "B3:H3"  
    cols = worksheet.get(cell_range)[0] #because of double list
    
    df_source = pd.read_csv(csv_source).transpose().iloc[1:] #to exclude the lost_phone_number heading
    col_name = df_source.iloc[0]
    df_source = df_source.iloc[1:] #to include the data only
    df_source.columns = col_name
    
    #Rearrange
    df_source_rearr = df_source[cols].reset_index()
    worksheet.append_rows(df_source_rearr.values.tolist())


# # Run

# In[5]:

#Comment out the variables
#json_cred = "your_json_apikey.json"
#url = "your_google_sheet_url"

#csv_unique_user = #"csv_filename_1.csv"
#num_sheet = 2

csv_source = #"csv_filename_2.csv"

#Execute the Initiate Function
spreadsheet = initiate(json_cred, url)

#Execute the Unique User Function
unique_user(spreadsheet, csv_unique_user, num_sheet)

#Execute the Split Source Function
source(spreadsheet, csv_source, num_sheet)


# In[ ]:





# In[ ]:





# In[ ]:




