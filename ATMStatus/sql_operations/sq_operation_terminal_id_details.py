from ViewATMStatus.db_connection_string import connection_string
from ATMStatus.properties.terminal_id_details_properties import TerminalIdDetailsProperties

class SqlTerminalIdDetails:


    def view_all_terminal_id_details(self):
        self.con_string = connection_string()
        self.query_set = 'exec sp_view_all_terminal_id_details'
        self.result = self.con_string.execute(self.query_set)
        return self.result
    
    # def view_particular_terminal_id_details(self,object_terminal_properties):
    #     con_string = connection_string()
    #     query_set = 'exec sp_get_particular_terminal_id_details @terminal_id=?'
    #     terminal_id = object_terminal_properties.terminal_id_getter()   
    #     result = con_string.execute(query_set,terminal_id)
    #     return result

    def add_terminal_id_details(self,object_terminal_properties):
        s_n = object_terminal_properties.s_n_getter()
        terminal_id = object_terminal_properties.terminal_id_getter()
        con_string = connection_string()
        query_set = 'exec sp_add_terminal_id_details @s_n=?,@terminal_id=?'
        values = [s_n,terminal_id]       
        result = con_string.execute(query_set,values)
        return result
        
    def get_particular_terminal_id_details(self,object_terminal_properties='default',id=0):
        con_string = connection_string()
        if object_terminal_properties == 'default':
            query_set = 'exec sp_get_particular_terminal_id_details @id=?,@terminal_id=?'             
            result = con_string.execute(query_set,id,object_terminal_properties)
            return result.fetchval()
        elif object_terminal_properties != 'default':
            query_set = 'exec sp_get_particular_terminal_id_details @id=?,@terminal_id=?'
            terminal_id = object_terminal_properties.terminal_id_getter()   
            result = con_string.execute(query_set,id,terminal_id)
            return result
      
    

    def total_row_count(self):
        con_string = connection_string()
        query_set = 'exec sp_get_total_row_count_terminal_id_details'
        result = con_string.execute(query_set)
        return result.fetchval()
    
    def get_update_data(self,id):
        con_string = connection_string()
        query_set = 'exec sp_get_data_for_update_terminal_id_details @id=?'
        # id = object_terminal_properties.terminal_id_getter()
        result = con_string.execute(query_set,id)
        return result.fetchall()

    def update_terminal_id_details(self,object_terminal_properties,id):
        con_string = connection_string()
        query_set = 'exec sp_update_data_terminal_id_details @id=?,@s_n=?,@terminal_id=?'
        s_n = object_terminal_properties.s_n_getter()      
        terminal_id = object_terminal_properties.terminal_id_getter()  
        values = [id,s_n,terminal_id]
        result = con_string.execute(query_set,values)
        return result
        

    def delete_terminal_id_details(self,id):
        con_string = connection_string()
        query_set = 'exec sp_delete_terminal_id_details @id=?'       
        result = con_string.execute(query_set,id)
        return result