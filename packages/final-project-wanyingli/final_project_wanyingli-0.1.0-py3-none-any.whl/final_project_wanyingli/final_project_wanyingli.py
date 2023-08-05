#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ## Part 1: Historical country lending data from the World Bank

# In[2]:


def get_wb_lending():
    """
    This API client function generates a Pandas DataFrame of the historical country lending data from the World Bank Project API. 
    The function takes the JSON format returned by the API and turns it into a Pandas DataFrame.
    It can generate up to 1500 projects information given the rate limits.
    API documentation: http://search.worldbank.org/api/v2/projects
    Authenticaiton: This API does not require a key and it is open for public use.
    
    Parameters (Inputs)
    ----------
    
    Returns (Output)
    -------
    Pandas Dataframe
        The output is a table of all country lending project containing project id, project name, project approval date, project total amount ($ millions), country code, country short name, and project URL.
    
    Examples
    --------
    >>> wb = get_wb_lending()
    >>> type(wb)
    pandas.core.frame.DataFrame
    
    """
    r = requests.get(f'http://search.worldbank.org/api/v2/projects?format=json&fl=boardapprovaldate,totalamt,countrycode&countryshortname&source=IBRD&rows=1500&frmYear=2008')
    if r.status_code != 200:
        print('API request is unsucessful!')
    elif r.status_code == 200:
        json = r.json()
        df = pd.DataFrame(json['projects'])
        df = df.transpose()
        df['countrycode'] = df['countrycode'].str.get(0)
        df['totalamt'] = df['totalamt'].str.replace(',', '')
        df['($) millions'] = (df['totalamt'].astype(float)/1000000)
        return df


# In[4]:


def get_wb_countryyear(countrycode, startyear, endyear):
    """
    This API client function returns a Pandas DataFrame and prints the total lending amount which allows users to search projects by a specific country and time period. 
    Please note that countrycodes are Alpha-2 code (which is two-letter code).
    please limit the time period within 2 years due to the rate limits of 1500 rows.
    
    
    Parameters (Inputs)
    ----------
    countrycode: str
       Two-letter Alpha-2 country code. Please go to https://www.iban.com/country-codes for more information
    
    startyear: int
       Enter the startyear of the projects you'd like to search for a given country. The earliest startyear is 1940.
    
    endyear: int
       Enter the endyear of the projects you'd like to search for a given country. The latest endyear is 2020.
    
    Returns (Output)
    -------
    Pandas Dataframe
        The output is a table of selected lending projects containing project id, project name, project approval date, project total amount ($ millions), country code, country short name, and project URL.
    
    Examples
    --------
    >>> get_wb_countryyear('CN', 2008, 2010) #this returns all projects received by China from 2008 to 2010.
    
    """
    r = requests.get(f'http://search.worldbank.org/api/v2/projects?format=json&fl=boardapprovaldate,totalamt,countrycode&countrycode_exact={countrycode}&countryshortname&source=IBRD&rows=1500&frmYear={startyear}&toYear={endyear}')
    if r.status_code != 200:
        print('API request is unsucessful!')
    elif r.status_code == 200:
        json = r.json()
        df = pd.DataFrame(json['projects'])
        df = df.transpose()
        df['countrycode'] = df['countrycode'].str.get(0)
        df['totalamt'] = df['totalamt'].str.replace(',', '')
        df['($) millions'] = (df['totalamt'].astype(float)/1000000)
        Total = (df['($) millions']).sum()
        print (f'The total lending amount received by {countrycode} from {startyear} to {endyear} is: ${Total} million')
        return df


# In[6]:


def get_wb_environment(environment_category, startyear, endyear):
    """
    This function returns a Pandas DataFrame and prints the total lending amount by querying a specific environmental standard and time period. 
    It allows the users to search for projects from the perspective of sustainable development.
    Please limit the time period within 2 years due to the rate limits of 1500 rows.
    

    Parameters (Inputs)
    ----------
    environment_category: str
       All possible categories are 'B','C','D','F','G','H','U'. 
       
    startyear: int
       Enter the startyear of the projects you'd like to search for a given environmental category. The earliest startyear is 1940.
    
    endyear: int
       Enter the endyear of the projects you'd like to search for a given environmental category. The latest endyear is 2020.
    
    
    Returns (Output)
    -------
    Pandas Dataframe
        The output is a table of selected lending projects containing project id, project name, project approval date, project total amount ($ millions), country code, country short name, and project URL.
    
    Examples
    --------
    >>> get_wb_environment('B', 2019, 2020) #this returns all projects with "B" environmental category from 2019 to 2020.
    
    """
    
    r = requests.get(f'http://search.worldbank.org/api/v2/projects?format=json&fl=boardapprovaldate,totalamt,countrycode,countryshortname&envassesmentcategorycode={environment_category}&source=IBRD&rows=100&frmYear={startyear}&toYear={endyear}')
    if r.status_code != 200:
        print('API request is unsucessful!')
    elif r.status_code == 200:
        json = r.json()
        df = pd.DataFrame(json['projects'])
        df = df.transpose()
        df['countrycode'] = df['countrycode'].str.get(0)
        df['totalamt'] = df['totalamt'].str.replace(',', '')
        df['($) millions'] = (df['totalamt'].astype(float)/1000000)
        Total = (df['($) millions']).sum()
        print (f'The total lending amount of projects with environmental category of {environment_category} from {startyear} to {endyear} is: ${Total} million')
        return df


# ## Part 2: Historical sovereign lending data from the Asian Development Bank (ADB)

# In[7]:


def get_adb_lending():
    """
    This function returns a Pandas DataFrame of the historical country lending data from the ADB from 2008 to 2020. 
    It accessed the dataset via a csv file since no API data is available for ADB projects, and turns it into a Pandas DataFrame.
    Web scrapping of Alpha-2 country code standard from https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2 to match with country name in the ADB project data.
    Alpha-2 country code is used here in order to be consistent with the parameters of World Bank API client functions. 

  
    Parameters (Inputs)
    ----------
    
    Returns (Output)
    -------
    Pandas Dataframe
        The output is a table of all ADB country lending project containing project name, project approval date, project total amount ($ millions), country code, and country short name.
    
    Examples
    --------
    >>> adb = get_adb_lending()
    >>> type(adb)
    pandas.core.frame.DataFrame
    
    """ 
    
    adb = pd.read_csv(r"C:\Users\wanyi\Downloads\adb-sov-projects-20200317.csv") 
    alpha2 = pd.read_html('https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2')[2]
    alpha2.replace(to_replace=r'\[\d*\]', value='', regex=True)  # remove footnotes
    alpha2 = alpha2[['Code', 'Country name (using title case)']]
    alpha2.columns = ['countrycode', 'Country']
    adb_all = adb.merge(alpha2, on='Country', how='left')
    adb_all = adb_all[['Project Name', 'ADB Financing (US$)', 'Country','countrycode', 'Approval Date']]
    adb_all['ADB Financing (US$)'] = adb_all['ADB Financing (US$)'].str.replace(',', '')
    adb_all['($) millions'] = (adb_all['ADB Financing (US$)'].astype(float)/1000000)
    return adb_all


# In[8]:


def get_adb_countryyear(countrycode, year):
    """
    This function generates a Pandas DataFrame and print the total project lending amounts. 
    It allows users to search for ADB projects received by a specific country in a specific year.
    
    
    Parameters (Inputs)
    ----------
    countrycode: str
       Two-letter Alpha-2 country code. Please go to https://www.iban.com/country-codes for more information. 
    
    year: int
       Enter the specific year of results you'd like to search for a given country. The earliest year is 2008.
           
       
    Returns (Output)
    -------
    Pandas Dataframe
        The output is a table of all ADB country lending projects containing project name, project approval date, project total amount ($ millions), country code, and country short name.
    
    Examples
    --------
    >>> get_adb_countryyear('NP', '2019') #this returns all projects received by Nepal in 2019
    
    """     
   
    df =get_adb_lending()
    df['Approval Date'] = df['Approval Date'].astype('datetime64[ns]')
    df['Approval Year'] = pd.DatetimeIndex(df['Approval Date']).year
    Total = (df['($) millions']).sum().round(2)
    print (f'The total lending amount received by {countrycode} is: ${Total} million')
    return df.loc[(df['countrycode']== countrycode) & (df['Approval Year'] == year)]


# In[9]:


def plot_adb_top10():
    """
    This function plots a bar chart of the top 10 recepient countries in terms of project amounts since 2008.
    
    Parameters (Inputs)
    ----------      
       
    Returns (Output)
    -------
    Plot
        The output is a bar chart of of the top 10 recepient countries over time.
    
    Examples
    --------
    >>> plot_adb_top10()
    The result is a bar chart.
    
    """     
    df =get_adb_lending()
    df =df.groupby('countrycode')['($) millions'].sum()[:10].reset_index()
    df=df.sort_values('($) millions')
    plt.bar(df['countrycode'],df['($) millions'], alpha = 0.5)
    plt.show()


# In[ ]:




