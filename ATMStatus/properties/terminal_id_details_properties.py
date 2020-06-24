
class TerminalIdDetailsProperties:
    s_n= ''
    terminal_id = ''

    # def setter(self,s_n,terminal_id):
    #     self.s_n =s_n
    #     self.terminal_id = terminal_id

    #     obj_terminal = TerminalIdDetailsProperties()
    #     non_value1 = obj_terminal.s_n_getter()         
    #     non_value2 = obj_terminal.terminal_id_getter()


    def s_n_getter(self):           
        return self.s_n
    
    def s_n_setter(self,s_n):
        self.s_n = s_n
    
    def terminal_id_getter(self):
        return self.terminal_id
    
    def terminal_id_setter(self, terminal_id):
        self.terminal_id = terminal_id


    