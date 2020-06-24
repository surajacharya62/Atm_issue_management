from ViewATMStatus import db_connection_string

def get_branch_name(branch_name):
   
    con_string =  db_connection_string.connection_string()
    query_set = 'exec sp_get_branch_name_branch_details @branch_name=?'
    branch_name = con_string.execute(query_set,branch_name)
    return branch_name.fetchval()
    
    

def get_total_number_of_row():
    try:
        con_string =  db_connection_string.connection_string()
        query_set = 'exec sp_count_all_rows'      
        total_row = con_string.execute(query_set)    
        total_count = total_row.fetchval()
        return total_count
    finally:
        con_string.close()

def get_branch_code(branch_code):
    
        con_string =  db_connection_string.connection_string()
        query_set = 'exec sp_get_branch_code_branch_details @branch_code=?'      
        branch_code = con_string.execute(query_set,branch_code)       
        return branch_code.fetchval()
   
    
'''
    Adds new branch details.
'''
def add_branch_details(s_n, branch_name, branch_code):
  
    con_string =  db_connection_string.connection_string()
    query_set = 'exec sp_add_branch_details @s_n=?,@branch_name=?,@branch_code=?'  
    print(branch_code)
    values = (s_n,branch_name,branch_code)   
    result = con_string.execute(query_set,values)     
    return result

   

'''
    Get particular branch details.
'''
def get_particular_branch_details(id):
    con_string = db_connection_string.connection_string()
    query_set = 'exec sp_get_praticular_branch_details @id = ?'
    result =  con_string.execute(query_set,id)
    return result

'''
    Update branch details.
'''
def update_branch_details(id,s_n,branch_name,branch_code):
    con_string = db_connection_string.connection_string()
    query_set  = 'exec sp_update_branch_details @id=?,@s_n=?,@branch_name=?,@branch_code=?'
    values = [id,s_n,branch_name,branch_code]
    result = con_string.execute(query_set,values)
    return result

'''
 Delete branch details.
'''
def delete_branch_details(id):
    print('delete')
    con_string = db_connection_string.connection_string()
    query_set = 'exec sp_delete_branch_details @id=?'
    result = con_string.execute(query_set,id)
    return result