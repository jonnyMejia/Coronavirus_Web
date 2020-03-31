# Library for the WebScrapping
from bs4 import BeautifulSoup
import requests # Library for HTTP
import pandas as ps # Library to use Dataframes objects
import datetime as dt # Library to manage tiempos y fechas
import numpy as np # Library to realize
# Url of the page
url = 'https://www.worldometers.info/coronavirus/'

# To get Html 
html = requests.get(url)

def scrapping(url):
    "to get dataset from the url"
    page = BeautifulSoup(html.content,"html.parser") # To get web page in Html
    table = page.find('table' , {'id':'main_table_countries_today' }) # To get table from the HTML with id 
    thead =  page.find('thead').find('tr') # To get thead from the table
    tbody = table.find('tbody') # To get tbody from the table 
    
    # To get header from thead
    names = thead.find_all('th') 
    names = [ x.text for x in names] # To get names from the header
    
    # To get rows from the tbody    
    data_row = tbody.find_all('tr')
    data= [x.find_all('td') for x in data_row] # To get data in html from the rows
    
    dataset = toDataset(data) # to extract text from data in html with Pandas
    dataset = ps.DataFrame(dataset,columns=names) # To get Dataframe with Pandas
    clearDataset(dataset) # Clear data for processing
    
    # To save in a .csv file with today's date
    dataset.to_csv('{:%d-%m-%Y.csv}'.format(dt.datetime.now()),index=False) 
    
    return dataset

    
def toDataset(data):
    "to extract text from data in html"
    dataset=[] # Declare empty dataset 
    temp=[] # Declare temporary list to store rows
    for row in data:
        for value in row:
            temp.append(value.text)
        dataset.append(temp.copy())
        temp = [] # To clear temporary list
    
    return dataset     

def clearDataset(dataset):
    "Clear data for processing"
    # To remove white space in empty cells
    for i in dataset:
        dataset[i]=dataset[i].str.strip()        
    
    dataset=dataset.replace('',np.NaN) # To replace cells tith empty strings in NaN
    
    # To recognize integers and floats
    for i in dataset:
        try:
            dataset[i]=dataset[i].str.replace(",","").astype(int)
        except:
            # Is a float 
            try:
                dataset[i]=dataset[i].str.replace(",","").astype(float)
            except:
                pass


# call to function scrapping()
dataset = scrapping(url)

# To get data of peru 
peru = dataset[dataset['Country,Other']=='Peru']
    



