"""
------------------------------------------------------------------------
Author: Branden Wheeler
__updated__ = "2020-11-21"
------------------------------------------------------------------------
"""
#Imports
import mysql.connector

"""
DB Class
Description: This class essentially creates an interface to interact with
             the database in which the financial statement data is being stored.
             The methods within the class allow someone to perform CRUD operations
             on the database.
         
Instance Variables:
    db - holds a connection to the database where the financial statement
         info is being stored
"""
class DB:
    
    def __init__(self):
        
        """Reading in login information from a text file
        In order to access a database we need a host, username, password
        and database name """
        file = open('credentials/credentials.txt', 'r')
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
    """
    table_exists Method
    Description: Checks to see if a table with a given name exists
                 within the database
    
    Parameters:
        name (String) - Contains the table name that is to be checked for existence
        
    Returns:
        result (boolean) - holds whether or not the table exists
    """
    def table_exists(self, name):
        
        dbcur = self.db.cursor()
        #Selects tables from the database with the given name
        dbcur.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = N\'" + name + "\'")        
        result = dbcur.fetchone() #Result will contain whether or not the database was able to 'fetch' a table with the given name """
                                  
        dbcur.close()
        return result
    
    """
    create_table Method
    Description: Creates a new table within the database with the given name
    
    Parameters:
        name (String) - Contains the title of the new table to be created
    """
    def create_table(self, name):
        
        dbcur = self.db.cursor()
        """Creates table with row_id as primary key,
        data for year one, year two, year three, and the type
        of document that is being stored """
        dbcur.execute("CREATE TABLE " + name + """
        (row_id INT AUTO_INCREMENT PRIMARY KEY,
        row_title VARCHAR(100),
        year_one VARCHAR(100),
        year_two VARCHAR(100),
        year_three VARCHAR(100),
        doc_type VARCHAR(100))""")
        
        dbcur.close()

    """
    add_row Method
    Description: Adds a single row to the specified table 
    
    Parameters:
        name (String) - The name of the table to which a row will be added
        row_title (String) - The title of the row to be added
        year1 (String) - The data to be inserted in the year1 field
        year2 (String) - The data to be inserted in the year2 field
        year3 (String) - The data to be inserted in the year3 field
        doc_type (String) - The type of financial document the data comes from
    """
    def add_row(self, name, row_title, year1, year2, year3, doc_type):
        
        dbcur = self.db.cursor()
        record = (row_title, year1, year2, year3, doc_type)           
        dbcur.execute("INSERT INTO " + name + " (row_title, year_one, year_two, year_three, doc_type) VALUES (%s, %s, %s, %s, %s)", record)
        
        self.db.commit() #Exeutes SQL query
        
        dbcur.close()
        
    """
    add_rows Method
    Description: Adds multiple rows to the specified table
    
    Parameters:
        name (String) - The name of the table to which the rows are to be added
        items (2d array of String) - First dimension contains each row of data
                                     Second dimension contains data within the row
        type (String) - The type of document the data comes from
    """
    def add_rows(self, name, items, type):
        
        dbcur = self.db.cursor()
        
        """Loops through each row to be added and executes the SQL query necessary
        to add it to the table"""
        for item in items:
            record = (item[0], item[1], item[2], item[3], type)
            dbcur.execute("INSERT INTO " + name + " (row_title, year_one, year_two, year_three, doc_type) VALUES (%s, %s, %s, %s, %s)", record)
            self.db.commit() #Executes SQL query
                
        dbcur.close()
        
    """
    delete_table Method
    Description: Removes a table with a specified name from the database
    
    Parameters:
        name (String) - Contains the table name that is to be removed
    """
    def delete_table(self, name):
        
        dbcur = self.db.cursor()
        dbcur.execute("DROP TABLE " + name) #Executes SQL query
        dbcur.close()
    
    """
    get_tables Method
    Description: Retrieves a list of tables that currently exist
                 within the database
                 
    Returns:
        tables (List of Strings) - Contains a list of table names within
                                   the database
    """
    def get_tables(self):
        
        dbcur = self.db.cursor()
        dbcur.execute("SHOW TABLES") #Executes SQL query
        
        tables = dbcur.fetchall() #Grabs all table names from database
        dbcur.close()
        return tables
    
    """
    get_by_doc_type Method
    Description: Gets all rows from the specified table that contain data from
                the desired doc type
                
    Parameters:
        name (String) - Contains the name of the table from which data will be retrieved
        type (String) - The type of document that we want data from
        
    Returns:
        items (2d array of String) - First dimension contains each table row retrieved
                                     Second dimension contains the data found in each row
    """
    def get_by_doc_type(self, name, type):
        
        dbcur = self.db.cursor()
        dbcur.execute("SELECT row_title, year_one, year_two, year_three FROM " + name + " WHERE doc_type = '" + type + "'")
        items = dbcur.fetchall() #Grabs a list of rows that match the query
        
        dbcur.close()
        
        return items
        
        
        
        