#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 17:08:56 2018

@author: sarfraz
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

#Set Headers for request to the website 
header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

#define counter for pages
page_number=1

#define columns for the pandas dataframe that will collect the data
dfcols = ['Job_Title', 'Ad_Body','Company_Website','Job_URL' ]

#Innitialize Dataframe
df = pd.DataFrame(columns=dfcols)

#Innitiate a loop which will be terminated on a specific condition using break command
while True:   
    #define uRL from where the tables will be scraped
    url = "https://www.ukstartupjobs.com?paged="+str(page_number)+"&feed=job_feed&job_types=graduate-entry%2Cexperienced%2Cfreelance%2Cinternship&search_location&job_categories=marketing%2Ccontent&search_keywords"
    
    #Fetch the page at the url using "requests" module
    page = requests.get(url, headers=header)
    
    soup = BeautifulSoup(page.text,'xml')
   
    items=soup.find_all('item')
    #end the while loop if there are no items in the response.
    if len(items)==0:
        break
    
    #Itereate over the links in item tag, and get details of the post
    for link in soup.find_all('item'):
        #extract the link to the job post
        job_link=link.find('link').text
        #extract the title of the job post
        Title=link.find('title').text
        #make a request to get the details of the post
        page=requests.get(link.find('link').text,headers=header)
        soup = BeautifulSoup(page.text,'lxml')
        #get the link to the company website from the job detail page
        website=soup.find('a',{'class':'website'})
        company_website=website['href']
        #get the description from the job details page
        description=soup.find('div', {'class':'job_description'})
        ad_description=description.text
        #append the gathered information to the dataframe
        df = df.append(
            pd.Series([Title, ad_description, company_website,job_link ], index=dfcols),
            ignore_index=True)
    #increament the poge counter to get the next job listing page    
    page_number=page_number+1
 
#Export the dataframe to excel.
df.to_excel("UKStartupjob_marketing.xlsx") 