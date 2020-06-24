from ViewATMStatus.db_connection_string import connection_string

class SqlAtmDetails:

    s_n = ''
    branch_name = ''
    branch_code = ''
    atm_terminal_id = ''          
    atm_location =  ''
    atm_address =  ''
    atm_ip_address = ''
    switch_ip_address = ''
    switch_port_number =  ''   
    atm_installed_date = ''

    def sql_view_atm_details(self):
        con_string = connection_string()
        query_set = 'exec sp_view_atm_details'
        result = con_string.execute(query_set)
        return result
    
    def sql_get_particular_atm_details(self,search_value):
        con_string = connection_string()
        query_set = 'exec sp_get_particular_atm_details @branch_code=?'
        branch_code = search_value
        print(search_value)
        result = con_string.execute(query_set,branch_code)
        return result
    
    def get_all_branch_code(self):
        con_string = connection_string()
        query_set = 'exec sp_get_all_branch_code_atm_details'        
        result = con_string.execute(query_set)
        return result
    
    def get_all_branch_name(self):
        con_string = connection_string()
        query_set = 'exec sp_get_all_branch_name_atm_details'        
        result = con_string.execute(query_set)
        return result
    
    def get_all_terminal_id(self):
        con_string = connection_string()
        query_set = 'exec sp_get_all_terminal_id_atm_details'        
        result = con_string.execute(query_set)
        return result
    
    def get_row_count_atm_details(self):
        con_string = connection_string()
        query_set = 'exec sp_get_all_row_count_atm_details'        
        result = con_string.execute(query_set)
        return result
    
    # def get_branch_name_id(self,branch_name):
    #     con_string = connection_string()
    #     query_set = 'exec sp_get_branch_id_from_branch_details'        
    #     result = con_string.execute(query_set,branch_name)
    #     return result.fetchval()
    
    # def get_terminal_id(self,terminal_id):
    #     con_string = connection_string()
    #     query_set = 'exec sp_get_terminal_id_from_atm_terminal_id_details'        
    #     result = con_string.execute(query_set,terminal_id)
    #     return result.fetchval()

    def get_branch_name(self,branch_name):
        con_string = connection_string()
        query_set = 'exec sp_get_branch_name_from_atm_details @branch_name=?'        
        result = con_string.execute(query_set,branch_name)
        return result.fetchval()
    
    def get_branch_code(self,branch_code):
        con_string = connection_string()
        query_set = 'exec sp_get_branch_code_from_atm_details @branch_code=?'        
        result = con_string.execute(query_set,branch_code)
        return result.fetchval()
    
    def get_terminal_id(self,terminal_id):
        con_string = connection_string()
        query_set = 'exec sp_get_terminal_id_from_atm_details @terminal_id=?'        
        result = con_string.execute(query_set,terminal_id)
        return result.fetchval()

    def add_atm_details(self,object_atm_details):
        con_string = connection_string()
        query_set = '''exec sp_add_atm_details 
                        @s_n=?,
                        @branch_name=?,
                        @branch_code=?,
                        @atm_terminal_id=?,
                        @atm_location=?,
                        @atm_address=?,
                        @atm_ip_address=?,
                        @switch_ip_address=?,
                        @switch_port_number=?,
                        @atm_installed_date=?
                    '''
        values = [
                    object_atm_details.s_n,
                    object_atm_details.branch_name,
                    object_atm_details.branch_code,
                    object_atm_details.atm_terminal_id,
                    object_atm_details.atm_location,
                    object_atm_details.atm_address,
                    object_atm_details.atm_ip_address,
                    object_atm_details.switch_ip_address,
                    object_atm_details.switch_port_number,
                    object_atm_details.atm_installed_date,
                    ]      
        result = con_string.execute(query_set,values)

        return result
    
    def get_data_for_update_atm_details(self,pid):
        con_string = connection_string()
        query_set = 'exec sp_get_data_for_update_atm_details @id=?'        
        result = con_string.execute(query_set,pid)
        return result

    def modify_data_atm_details(self,object_atm_details,pid):
        con_string = connection_string()
        query_set = '''exec sp_update_atm_details 
                            @id=?,
                            @s_n=?,
                            @branch_name=?,
                            @branch_code=?,
                            @atm_terminal_id=?,
                            @atm_location=?,
                            @atm_address=?,
                            @atm_ip_address=?,
                            @switch_ip_address=?,
                            @switch_port_number=?,
                            @atm_installed_date=?
                        '''
        values = [
                        pid,
                        object_atm_details.s_n,
                        object_atm_details.branch_name,
                        object_atm_details.branch_code,
                        object_atm_details.atm_terminal_id,
                        object_atm_details.atm_location,
                        object_atm_details.atm_address,
                        object_atm_details.atm_ip_address,
                        object_atm_details.switch_ip_address,
                        object_atm_details.switch_port_number,
                        object_atm_details.atm_installed_date,
                 ]

        result = con_string.execute(query_set,values)    
        
        return result

    def delete_atm_details(self,pid):
        con_string = connection_string()
        query_set = 'exec sp_delete_atm_details @id=?'        
        result = con_string.execute(query_set,pid)
        return result

    def view_branchname_for_delete(self,pid):
        con_string = connection_string()
        query_set = 'exec sp_view_branch_name_for_delete_atm_details @id=?'        
        result = con_string.execute(query_set,pid)
        return result.fetchval()