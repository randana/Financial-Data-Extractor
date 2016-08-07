"""
Created on Sat Jul 16 15:49:22 2016

@author: arushdixit

The Program takes NSE Company Code as Input and returns the following values:
Name
Current Price
EBIT
Enterprise value
Return on Captal
Return on invested capital.
Debt to Equity Ratio
Market capitalisation
Net Block Previous Year
Working Capital
Price by Book ratio
Price by earnings ratio
Revenues
Earnings yield
"""

from bs4 import BeautifulSoup
import urllib2
import re
import csv

def readfile( filename , i):
    "File read utility"
    file = open(filename+str(i)+'.html')
    
    return file

def stripCompanyCode(company_code_url):
    company_code_url = company_code_url.replace('https://www.screener.in/company/','')
    company_code_url = company_code_url.replace('/','')
    company_code_url = company_code_url.replace('consolidated','')
            
    return company_code_url
    
def extractCompanyCodeFromScreenerTable(table):
    "This function extracts the Country Codes from Screener Table"
    company_code_url = []
    company_code_hash = {}
    for a in table.find_all('a', href=re.compile('https://www.screener.in/company/')):  
        company_code_hash.update({a.string:stripCompanyCode(a['href'])})
    
    return company_code_hash

def extractAllCompanyData(table, all_company_data):
    "This function extracts all the financial data from Screener Table"
    all_data = []
    
    for row in table.find_all('tr'):
        col = row.find_all('td')
        record = ''    
        for col_name in col:
            if col_name.string != None:
                record = record + '|' + col_name.string.strip()            
        all_company_data.append(record[1:])
                        
    return 

def setHeader(table):
    "This function sets the header from Screener Table"
    
    head = table.thead
    col_names = head.find_all('div', {'class': 'tooltip-inner'})
    col_name_list = ''
    
    for col_name in col_names:
        if col_name.string != None:
            col_name_list = col_name_list + str(col_name.string.encode('utf-8')) +'|'
            
    return col_name_list[:-1]

def writeFile(file_name, data):
    for item in data:
        file_name.write("%s\n" % item)

def isNan(name):
    if name == 'NaN':
        return 1
    else:
        return 0
        
def unicode_to_ascii(data):
    return data.encode('ascii','ignore')
    
def nanFinder(all_company_data, header):
    i = 0
    for data_row in all_company_data:
        j = 0
        list_of_nan_in_1_row = []
    
        for data_element in data_row:
            if data_element == 'NaN':
                list_of_nan_in_1_row.append(header[j])
            j = j + 1
    
        if list_of_nan_in_1_row:
            list_of_nan.update({all_company_data[i][0]:list_of_nan_in_1_row})
        i = i + 1
    return list_of_nan

def nanCompanyCodeExtractor(list_of_nan, company_code_hash):
    nan_with_company_code = {}
    nan_companies = list_of_nan.keys()
    for company in nan_companies:
        if not company_code_hash[company].isdigit():
            nan_with_company_code.update({company_code_hash[company]:list_of_nan[company]})
    return nan_with_company_code
######################
#        main        #
######################

all_company_data = []
all_company_data_ascii = []
company_code_hash = {}
header = []

#Extracting all company data
for i in range(1,10):
    html = readfile('Source/MarketCap',i)
    soup = BeautifulSoup(html,"html.parser")
    table = soup.find('table', {'class': 'table table-striped'})
    #Set Header
    if (i == 1):
        header = setHeader(table)
        all_company_data.append(header)
    extractAllCompanyData(table, all_company_data)
    company_code_hash.update(extractCompanyCodeFromScreenerTable(table))

#Writing output csv file
screener_data_file = open('screener_initial.txt', 'w') 
writeFile(screener_data_file, all_company_data)

#Converting unicode input data to string
for data in all_company_data:
    ascii_data = unicode_to_ascii(data)
    all_company_data_ascii.append(ascii_data) 

#Identifying NaN data elements
all_company_data = []
header = header.split('|')
for data in all_company_data_ascii:
    temp = data.split('|')
    all_company_data.append(temp)

list_of_nan = {}    #contains{company_name:header_col_name}
list_of_nan = nanFinder(all_company_data, header)

#NaN value Company Code Extractor to be used by scraper
nan_with_company_code = nanCompanyCodeExtractor(list_of_nan, company_code_hash)
print nan_with_company_code