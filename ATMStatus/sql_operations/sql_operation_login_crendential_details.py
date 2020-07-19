from ViewATMStatus.db_connection_string import connection_string


class SqlLoginCredentialdetails:

    s_n = ''
    branch_code_id = ''
    atm_ip = ''
    vnc_password = ''
    r_admin_user_name = ''
    r_admin_password = ''
    atm_journal_user_name = ''
    atm_journal_password = ''

    def view_login_credential_details(self):
        con_string = connection_string()
        query = 'exec sp_view_login_credential_details'
        result = con_string.execute(query)
        return result

    def get_particular_login_details(self, search_value_branch_code):
        con_string = connection_string()
        query = 'exec sp_get_particular_login_credential_details @branch_code=?'
        result = con_string.execute(query, search_value_branch_code)
        return result

    def get_all_branch_code(self):
        con_string = connection_string()
        query = 'exec sp_get_all_branch_code_atm_details'
        result = con_string.execute(query)
        return result.fetchall()

    def get_all_atm_ip(self):
        con_string = connection_string()
        query = 'exec sp_get_all_atm_ip_login_details'
        result = con_string.execute(query)
        return result.fetchall()

    def get_total_row_count(self):
        con_string = connection_string()
        query = 'exec sp_get_all_row_count_login_details'
        result = con_string.execute(query)
        return result.fetchval()

    def get_branch_code(self, branch_code):
        con_string = connection_string()
        query = 'exec sp_get_branch_code_login_details @branch_code=?'
        result = con_string.execute(query, branch_code.branch_code_id)
        return result.fetchval()

    def get_atm_ip(self, atm_ip):
        con_string = connection_string()
        query = 'exec sp_get_atm_ip_login_details @atm_ip=?'
        result = con_string.execute(query, atm_ip)
        return result.fetchval()

    def add_login_details(self, object_login_details):
        con_string = connection_string()
        values = [
            object_login_details.s_n,
            object_login_details.branch_code_id,
            object_login_details.atm_ip,
            object_login_details.vnc_password,
            object_login_details.r_admin_user_name,
            object_login_details.r_admin_password,
            object_login_details.atm_journal_user_name,
            object_login_details.atm_journal_password
        ]
        query = '''exec [sp_add_login_credential_details]
        @s_n =?,
        @branch_code=?,
        @atm_ip=?,
        @vnc_password=?,
        @r_admin_user_name=?,
        @r_admin_password=?,
        @atm_journal_user_name=?,
        @atm_journal_password=?
        '''
        result = con_string.execute(query, values)
        return result

    def get_data_for_update(self, pid):
        con_string = connection_string()
        query = 'exec sp_get_data_for_update_login_details @id=?'
        result = con_string.execute(query, pid)
        return result

    def update_login_details(self, object_login_details):
        con_string = connection_string()
        values = [
            object_login_details.s_n,
            object_login_details.branch_code_id,
            object_login_details.atm_ip,
            object_login_details.vnc_password,
            object_login_details.r_admin_user_name,
            object_login_details.r_admin_password,
            object_login_details.atm_journal_user_name,
            object_login_details.atm_journal_password
        ]
        query = '''exec [sp_update_login_credential_details]
        @s_n =?,
        @branch_code=?,
        @atm_ip=?,
        @vnc_password=?,
        @r_admin_user_name=?,
        @r_admin_password=?,
        @atm_journal_user_name=?,
        @atm_journal_password=?
        '''
        result = con_string.execute(query, values)
        return result

    def delete_atm_login_details(self, pid):
        con_string = connection_string()
        query = 'exec sp_delete_login_details @id=?'
        result = con_string.execute(query, pid)
        return result
        
    def get_branch_code_for_delete(self,pid):
        con_string = connection_string()
        query = 'exec sp_get_branch_code_for_delete_login_details @id=?'
        result = con_string.execute(query, pid)
        return result.fetchval()