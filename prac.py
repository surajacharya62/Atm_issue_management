# import pyodbc

# # for driver in pyodbc.drivers():
# #     print(driver)

# listt= [['suraj',1000],
#         ['Hanuman',21111]]
# server_name  = 'DESKTOP-1GSF8FJ\\SQLEXPRESS'
# database_name = 'atmmanagementdb'

# # cnx =  pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER= '+ server_name+';\DATABASE ='+ database_name+';UID=sa;PWD=password;\Trusted_connection=yes;')
# cnx = pyodbc.connect(driver = '{ODBC Driver 17 for SQL Server}',
#  host=server_name,
#  database=database_name,
#  user='sa',
#  password='password',
#  trusted_connection = 'no'
#  )

# cusor = cnx.cursor()

# insert_query = '''
#     insert into tbl_test(name,number)
#     values(?,?)
# '''
# sp = "exec proc_test @name=?, @number=?"

# for val in listt:
#     values= (val[0],val[1] )
#     # cusor.execute(insert_query,values)
#     cusor.execute(sp,values)


# qr = 'select * from tbl_test'
# cusor.execute(qr)
# vals = cusor.fetchval()
# for val in cusor:
#     print(val)
# cnx.commit()
# print(cnx.commit())

def main():
    print('first module-{}'.format(__name__))


if __name__ == '__main__':
    main()

else:
    print('run from import.')
