"""
------------------------------------------------------------------------
This program will allow a user to enter a company's name or symbol. It will then search Yahoo
Finance for the provided name and symbol and use web scraping to extract data about the company.
The information will then be saved into an Excel spreadsheet

Selenium is being used to automate the rich browser tasks such as using the search bar
Beautiful Soup is being used for web scraping and collecting relevant data
Pandas is being used to move the data into a spreadsheet format
------------------------------------------------------------------------
Author: Branden Wheeler
__updated__ = "2020-09-09"
------------------------------------------------------------------------
"""
#Imports
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

"""
AddCompany Class
Description: This class facilitates the webscraping of a company's financial
             data from Yahoo Finance. It pulls the income statement, balance
             sheet, and cash flow statement from the company page and stores
             each in a 2d array.
         
Instance Variables:
    driver - contains the webdriver object that allows Selenium to interact with
             Google Chrome
    symbol - contains the stock symbol of the company for which the user wants
             financial statement info
    income_data - this is a 2d array that stores the income statement data pulled
                  from Yahoo Finance
    balance_data - this is a 2d array that stores the balance sheet data pulled
                   from Yahoo Finance
    cash_data - this is a 2d array that stores the statement of cash flow data
                pulled from Yahoo Finance
"""
class AddCompany:
    
    PATH = "C:\Program Files (x86)\chromedriver.exe" #Location on hard drive of chromedriver
    
    def __init__(self, namesym):
        #Initializing instance variables
        self.driver = webdriver.Chrome(self.PATH)
        self.driver.minimize_window() #Closing chrome window so it isn't over application
        self.symbol = namesym
        self.income_data = []
        self.balance_data = []
        self.cash_data = []
        
    """
    fix_lists Method
    Description: This method fixes the headers for each statement to only have the years
                 from the dates and removes any unnecessary lines that were pulled from
                Yahoo Finance. This ensures standardization for entering data into the
                database
    """
    def fix_lists(self):
    
        #Keeps 3 years of data, removes series title and TTM data for headers
        self.income_data[0] = self.income_data[0][2:5]
        self.balance_data[0] = self.balance_data[0][1:4]
        self.cash_data[0] = self.cash_data[0][2:5]
        
        """
        Loops through each header for each statement and converts the date
        from MM/DD/YYYY to just the 4 digit year
        """
        for i in range(0,3):
            #The 3rd item when splitting by '/' will be the year
            self.income_data[0][i] = self.income_data[0][i].split('/')[2]
            self.balance_data[0][i] = self.balance_data[0][i].split('/')[2]
            self.cash_data[0][i] = self.cash_data[0][i].split('/')[2]
            
        """ Loops through each row in the income statement data and trims off the 
        TTM data """
        for i in range(len(self.income_data)):
            """ Checking to see if TTM data exists in this row which would
            make the length greater than 3. Also helps to skip over headings
            which were previously reduced to a length of 3 """
            if len(self.income_data[i]) > 3:
                self.income_data[i].pop(1)
                self.income_data[i] = self.income_data[i][:4]
         
        """ Loops through each row in the balance sheet data and trims off the 
        TTM data """       
        for i in range(len(self.balance_data)):
            """ Checking to see if TTM data exists in this row which would
            make the length greater than 3. Also helps to skip over headings
            which were previously reduced to a length of 3 """
            if len(self.balance_data[i]) > 3:
                self.balance_data[i] = self.balance_data[i][:4]
        
        """ Loops through each row in the cash flow data and trims off the 
        TTM data """       
        for i in range(len(self.cash_data)):
            """ Checking to see if TTM data exists in this row which would
            make the length greater than 3. Also helps to skip over headings
            which were previously reduced to a length of 3 """
            if len(self.cash_data[i]) > 3:
                self.cash_data[i].pop(1)
                self.cash_data[i] = self.cash_data[i][:4]
            
    """
    page_navigate Method
    Description: This method utilizes the Chrome driver to navigate to a given URL
    """   
    def page_navigate(self, url):
        self.driver.get(url) #Navigating to given url
        
    """
    grab_income Method
    Description: This method navigates to the income statement page of the requested company
    scrapes the html from the page, and parses it to pick out the information from the
    desired table
    """
    def grab_income(self):
        
        self.page_navigate('https://finance.yahoo.com/quote/' + self.symbol + '/financials?p=' + self.symbol)
        time.sleep(10) #Need to wait to ensure data fully loads
        html = self.driver.execute_script('return document.body.innerHTML;') #Grabbing html from page
        income_soup = BeautifulSoup(html, 'lxml')
        entries = income_soup.find_all('div', class_='D(tbr)') #Grabs any div tags from the table row class
    
        headers = []
        """This loop collects the headers of the columns and puts them in a list
        all headers are found as the first item in the list of entries generated
        """
        for item in entries[0].find_all('div', class_='D(ib)'):
            headers.append(item.text)
            
        self.income_data.append(headers)
        index = 0
        """This loop goes through each of the entries in the table in order to collect
        the data """
        while index <= len(entries)-1:
    
            temp = [] #Resetting temp to fill up with next row 
            #Finds the tags containing the class indicating where the actual data is stored
            lines = entries[index].find_all('div', class_='D(tbc)')
            """This loop goes through each of the values in the current row and appends
            it to a list """
            for line in lines:
                temp.append(line.text)
    
            #Ensuring empty rows are not inserted into the table
            if temp != []:
                self.income_data.append(temp) #Creating a 2D list of temp lists that are generated above
                
            index+=1
            
    """
    grab_balance Method
    Description: This method navigates to the balance sheet page of the requested company
    scrapes the html from the page, and parses it to pick out the information from the
    desired table
    """        
    def grab_balance(self):
        
        self.page_navigate('https://finance.yahoo.com/quote/' + self.symbol + '/balance-sheet?p=' + self.symbol)
        
        time.sleep(10) #Need to wait to ensure data fully loads
        html = self.driver.execute_script('return document.body.innerHTML;') #Grabbing html from page
        balance_soup = BeautifulSoup(html, 'lxml')
        entries = balance_soup.find_all('div', class_='D(tbr)') #finds all div tags under the table row class
    
        headers = []
        """This loop collects the headers of the columns and puts them in a list
        all headers are found as the first item in the list of entries generated
        """
        for item in entries[0].find_all('div', class_='D(ib)'):
            headers.append(item.text)
                    
        
        self.balance_data.append(headers)
        
        index = 0
        """This loop goes through each of the entries in the table in order to collect
        the data """
        while index <= len(entries)-1:
            temp = []
            #Finds the tags containing the class indicating where the actual data is stored
            lines = entries[index].find_all('div', class_='D(tbc)')
            """This loop goes through each of the values in the current row and appends
            it to a list """
            for line in lines:
                temp.append(line.text)
    
            #Ensuring empty rows are not inserted to the table
            if temp != []:
                self.balance_data.append(temp) #Creating a 2D list of temp lists that are generated above
                
            index+=1
            
    """
    grab_cash Method
    Description: This method navigates to the cash flow page of the requested company
    scrapes the html from the page, and parses it to pick out the information from the
    desired table
    """ 
    def grab_cash(self):
        
        self.page_navigate('https://finance.yahoo.com/quote/' + self.symbol + '/cash-flow?p=' + self.symbol)
        
        time.sleep(10) #Need to wait to ensure data fully loads
        html = self.driver.execute_script('return document.body.innerHTML;') #Grabbing html from page
        balance_soup = BeautifulSoup(html, 'lxml')
        entries = balance_soup.find_all('div', class_='D(tbr)') #finds all div tags under the table row class
    
        headers = []
        """This loop collects the headers of the columns and puts them in a list
        all headers are found as the first item in the list of entries generated
        """
        for item in entries[0].find_all('div', class_='D(ib)'):
            headers.append(item.text)
        
        self.cash_data.append(headers)
    
        index = 0
        """This loop goes through each of the entries in the table in order to collect
        the data """
        while index <= len(entries)-1:
    
            temp = []
            #Finds the tags containing the class indicating where the actual data is stored
            lines = entries[index].find_all('div', class_='D(tbc)')
            """This loop goes through each of the values in the current row and appends
            it to a list """
            for line in lines:
                temp.append(line.text)
    
            #Ensures blank rows are not added to the table
            if temp != []:
                self.cash_data.append(temp) #Creating a 2D list of temp lists that are generated above
                
            index+=1
    
    """
    use Method
    Description: This method is called to run almost all methods in the class in order
    to go through the whole process of collecting all data from the requested company.
    It grabs info from each statement, fixes the lists, and quits. This ensures only
    one method call needs to be used to perform the full functionality 
    """
    def use(self):
        self.grab_income()
        self.grab_balance()
        self.grab_cash()
        self.fix_lists()
        self.quit()
        
    """
    quit Method
    Description: This method simply closes the chrome driver causing the 
    instance of the Google Chrome browser to disappear
    """
    def quit(self):
        self.driver.quit()
    
    """
    test Method
    Description: Allows the programmer to test the functioning of the
    object by allowing them to see the data that was collected from Yahoo
    in the console. Used purely for testing purposes
    """        
    def test(self):
        
        print("Income Data:")
        for item in self.income_data:
            print(item)
            
        print("\nBalance Data:")
        for item in self.balance_data:
            print(item)
            
        print("\nCash Data:")
        for item in self.cash_data:
            print(item)

