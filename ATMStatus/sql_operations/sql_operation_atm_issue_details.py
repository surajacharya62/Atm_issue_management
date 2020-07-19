from ViewATMStatus.db_connection_string import connection_string


class SqlAtmIssueDetails:

    s_n = ''
    issue_no_id = ''
    sub_issue_no = ''
    branch_code = ''
    terminal_id = ''
    problem = ''
    remarks = ''
    atm_issue_priority = ''
    issue_date = ''

    def view_all_issue_details(self):
        con_string = connection_string()
        query_set = 'exec sp_view_atm_issue_details'
        result = con_string.execute(query_set)
        return result

    def get_particular_issue_details(self, search_value):
        con_string = connection_string()
        query_set = 'exec sp_get_particular_atm_issue_details @search_value=?'
        result = con_string.execute(query_set, search_value)
        return result

    def get_all_branch_code(self):
        con_string = connection_string()
        query_set = 'exec sp_get_all_branch_code_atm_details'
        result = con_string.execute(query_set)
        return result

    def get_all_terminal_id(self):
        con_string = connection_string()
        query_set = 'exec sp_get_all_terminal_id_atm_details'
        result = con_string.execute(query_set)
        return result

    def get_total_row_count(self):
        con_string = connection_string()
        query_set = 'exec sp_get_total_row_count_atm_issue_details'
        result = con_string.execute(query_set)
        return result

    def add_atm_issue_details(self, object_atm_issue_details):
        con_string = connection_string()
        query_set = '''exec sp_add_atm_issue_details
                     @s_n=?,
                     @branch_code=?,
                     @terminal_id=?,
                     @problem=?,
                     @remarks=?,
                     @atm_issue_priority=?,
                     @issue_date=?'''
        values = [
            object_atm_issue_details.s_n,
            object_atm_issue_details.branch_code,
            object_atm_issue_details.terminal_id,
            object_atm_issue_details.problem,
            object_atm_issue_details.remarks,
            object_atm_issue_details.atm_issue_priority,
            object_atm_issue_details.issue_date
        ]

        result = con_string.execute(query_set, values)
        return result

    def get_data_for_update(self, pid):
        con_string = connection_string()
        query_set = 'exec sp_get_data_for_update_atm_issue_details @id = ?'
        result = con_string.execute(query_set, pid)
        return result

    def update_atm_issue_details(self, object_atm_issue_details, id):
        con_string = connection_string()
        query_set = '''exec sp_update_atm_issue_details
                     @id=?,
                     @s_n=?,
                     @branch_code=?,
                     @terminal_id=?,
                     @problem=?,
                     @remarks=?,
                     @atm_issue_priority=?,
                     @issue_date=?'''
        values = [
            id,
            object_atm_issue_details.s_n,
            object_atm_issue_details.branch_code,
            object_atm_issue_details.terminal_id,
            object_atm_issue_details.problem,
            object_atm_issue_details.remarks,
            object_atm_issue_details.atm_issue_priority,
            object_atm_issue_details.issue_date
        ]

        result = con_string.execute(query_set, values)
        return result

    def delete_atm_issue_details(self, id):
        con_string = connection_string()
        query_set = 'exec sp_delete_atm_issue_details @id=?'
        result = con_string.execute(query_set, id)
        return result

    def get_branch_code(self, object_atm_issue_details):
        con_string = connection_string()
        query_set = 'exec sp_get_branch_code_atm_issue_details @branch_code=?'
        branch_code = object_atm_issue_details.branch_code
        result = con_string.execute(query_set, branch_code)
        return result.fetchval()

    def view_sub_atm_issue_details(self, pid):
        con_string = connection_string()
        query_set = 'exec sp_view_sub_atm_issue_details @id=?'
        result = con_string.execute(query_set, pid)
        return result

    def get_sub_issue_no(self, pid):
        con_string = connection_string()
        query_set = 'exec sp_get_row_count_sub_atm_issue_details @id=?'
        result = con_string.execute(query_set, pid)
        return result.fetchval()

    def get_branch_terminal_details(self, pid):
        con_string = connection_string()
        query_set = 'exec sp_get_branch_terminal_sub_atm_issue_details @id=?'
        result = con_string.execute(query_set, pid)
        return result

    def add_sub_atm_issue_details(self, object_atm_issue_details):
        con_string = connection_string()
        query_set = '''exec sp_add_sub_atm_issue_details
                     @issue_no_id=?,
                     @sub_issue_no=?,
                     @branch_code_id=?,
                     @terminal_id=?,
                     @problem=?,
                     @remarks=?,
                     @atm_issue_priority=?,
                     @issue_date=?'''
        values = [

            object_atm_issue_details.issue_no_id,
            object_atm_issue_details.sub_issue_no,
            object_atm_issue_details.branch_code,
            object_atm_issue_details.terminal_id,
            object_atm_issue_details.problem,
            object_atm_issue_details.remarks,
            object_atm_issue_details.atm_issue_priority,
            object_atm_issue_details.issue_date
        ]

        result = con_string.execute(query_set, values)
        return result
