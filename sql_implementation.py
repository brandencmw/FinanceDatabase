"""
------------------------------------------------------------------------
[program description]
------------------------------------------------------------------------
Author: Branden Wheeler
ID:     190197360
Email:  whee7360@mylaurier.ca
__updated__ = "2019-09-27"
------------------------------------------------------------------------
"""
import mysql.connector

class DB:
    
    def __init__(self):
        
        file = open('credentials.txt', 'r')
        host_line = file.readline().strip()[5:]
        user_line = file.readline().strip()[5:]
        password_line = file.readline().strip()[9:]
        database_line = file.readline().strip()[9:]
        
        file.close()
        
        
        self.db = mysql.connector.connect(
            host = host_line,
            user=user_line,
            password=password_line,
            database=database_line)
        
    def tableExists(self, name):
        
        dbcur = self.db.cursor()
        dbcur.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = N\'" + name + "\'")        
        result = dbcur.fetchone()
        dbcur.close()
        return result
    
    def createTable(self, name, adder):
        
        dbcur = self.db.cursor()
        dbcur.execute("CREATE TABLE " + name + """
        (row_title VARCHAR(100) PRIMARY KEY,
        year_one VARCHAR(100),
        year_two VARCHAR(100),
        year_three VARCHAR(100),
        doc_type VARCHAR(100))""")
        
        dbcur.close()

    def addRow(self, name, row_title, year1, year2, year3, doc_type):
        
        dbcur = self.db.cursor()
        #query = "insert into " + name + " (row_title, year_one, year_two, year_three, doc_type) VALUES('Heading', '2019', '2018', '2017', 'Income')"
        #print(query)   
        record = (row_title, year1, year2, year3, doc_type)           
        dbcur.execute("INSERT INTO " + name + " (row_title, year_one, year_two, year_three, doc_type) VALUES (%s, %s, %s, %s, %s)", record)
        
        self.db.commit()
        
        dbcur.close()
        
    def addRows(self, name, items, type):
        
        dbcur = self.db.cursor()
        for item in items:
            record = (item[0], item[1], item[2], item[3], type)
            print(record)
            dbcur.execute("INSERT INTO " + name + " (row_title, year_one, year_two, year_three, doc_type) VALUES (%s, %s, %s, %s, %s)", record)
            self.db.commit()
                
        dbcur.close()
    def deleteTable(self, name):
        
        dbcur = self.db.cursor()
        dbcur.execute("DROP TABLE " + name)
        dbcur.close()
        
    def get_tables(self):
        
        dbcur = self.db.cursor()
        dbcur.execute("SHOW TABLES")
        
        tables = dbcur.fetchall()
        dbcur.close()
        return tables
        
        
        