import pyodbc

# for driver in pyodbc.drivers():
#     print(driver)


server_name  = 'DESKTOP-SCDJ7I2\SQLEXPRESS'
database_name = 'db_atmmanagement'
user= 'sa'
password='Crack#342'
trusted_connection ='no'

'''
Database connection strings.
'''
cursor = ''
def connection_string(): 
    connection_string = pyodbc.connect(
        driver = '{ODBC Driver 17 for SQL Server}',
        host = server_name,
        database = database_name,
        user = user,
        password = password,
        trusted_connection = trusted_connection
    )
    cursor = connection_string.cursor()
    return cursor

   
    
        




