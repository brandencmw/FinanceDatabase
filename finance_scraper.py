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


class AddCompany:
    
    PATH = "C:\Program Files (x86)\chromedriver.exe" #Location on hard drive of chromedriver
    
    def __init__(self, namesym):
        self.driver = webdriver.Chrome(self.PATH)
        self.driver.minimize_window()
        self.symbol = namesym
        self.income_data = []
        self.balance_data = []
        self.cash_data = []
        
    def fix_lists(self):
    
        self.income_data[0] = self.income_data[0][2:5]
        self.balance_data[0] = self.balance_data[0][1:4]
        self.cash_data[0] = self.cash_data[0][2:5]
        
        for i in range(0,3):
            self.income_data[0][i] = self.income_data[0][i].split('/')[2]
            self.balance_data[0][i] = self.balance_data[0][i].split('/')[2]
            self.cash_data[0][i] = self.cash_data[0][i].split('/')[2]
            
        for i in range(len(self.income_data)):
            if len(self.income_data[i]) > 3:
                self.income_data[i].pop(1)
                self.income_data[i] = self.income_data[i][:4]
                
        for i in range(len(self.balance_data)):
            if len(self.balance_data[i]) > 3:
                self.balance_data[i] = self.balance_data[i][:4]
                
        for i in range(len(self.cash_data)):
            if len(self.cash_data[i]) > 3:
                self.cash_data[i].pop(1)
                self.cash_data[i] = self.cash_data[i][:4]
        
        self.test()
            
        
    def page_navigate(self, url):
        self.driver.get(url) #Navigating to Yahoo finance main page
        
    def grab_income(self):
        
        self.page_navigate('https://finance.yahoo.com/quote/' + self.symbol + '/financials?p=' + self.symbol)
        time.sleep(10) #Need to wait to ensure data fully loads
        html = self.driver.execute_script('return document.body.innerHTML;') #Grabbing html from page
        income_soup = BeautifulSoup(html, 'lxml')
        entries = income_soup.find_all('div', class_='D(tbr)')
    
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
    
            if temp != []:
                self.income_data.append(temp) #Creating a 2D list of temp lists that are generated above
                
            index+=1
            
            
    def grab_balance(self):
        
        self.page_navigate('https://finance.yahoo.com/quote/' + self.symbol + '/balance-sheet?p=' + self.symbol)
        
        time.sleep(10) #Need to wait to ensure data fully loads
        html = self.driver.execute_script('return document.body.innerHTML;') #Grabbing html from page
        balance_soup = BeautifulSoup(html, 'lxml')
        entries = balance_soup.find_all('div', class_='D(tbr)')
    
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
    
            if temp != []:
                self.balance_data.append(temp) #Creating a 2D list of temp lists that are generated above
                
            index+=1
            
    
    def grab_cash(self):
        
        self.page_navigate('https://finance.yahoo.com/quote/' + self.symbol + '/cash-flow?p=' + self.symbol)
        
        time.sleep(10) #Need to wait to ensure data fully loads
        html = self.driver.execute_script('return document.body.innerHTML;') #Grabbing html from page
        balance_soup = BeautifulSoup(html, 'lxml')
        entries = balance_soup.find_all('div', class_='D(tbr)')
    
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
    
            if temp != []:
                self.cash_data.append(temp) #Creating a 2D list of temp lists that are generated above
                
            index+=1
            
    def use(self):
        self.grab_income()
        self.grab_balance()
        self.grab_cash()
        self.fix_lists()
        self.quit()
        
    def quit(self):
        self.driver.quit()
            
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

