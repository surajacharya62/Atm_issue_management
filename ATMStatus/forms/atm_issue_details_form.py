from django import forms
from ATMStatus.models import AtmIssueDetails, BranchDetails
from ATMStatus.sql_operations.sql_operation_atm_issue_details import SqlAtmIssueDetails


class MyDateInput(forms.DateInput):
    input_type = 'date'

class AtmIssueDetailsForm(forms.Form):

    object_sql_atm_issue_details =  SqlAtmIssueDetails()
    query_result_branch_code = object_sql_atm_issue_details.get_all_branch_code()
    query_result_terminal_id = object_sql_atm_issue_details.get_all_terminal_id()

    branch_code_choices = [(branchCode.id, branchCode.branch_code)
                      for branchCode in query_result_branch_code]
    atm_terminal_id_choices  = [(terminalId.id,terminalId.terminal_id) for terminalId in query_result_terminal_id ]

    CHOICES = [('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')]
    s_n = forms.IntegerField()
    # branch_name = forms.ForeignKey(
    #     BranchDetails, on_delete=models.CASCADE, null=True, related_name='AtmIssuedDetails_branch_name')
    
    branch_code = forms.ChoiceField(required=True, choices=[(
        None, 'Please select branch code')]+branch_code_choices)
    terminal_id = forms.ChoiceField(required=True, choices=[(
        None, 'Please select terminal id')]+atm_terminal_id_choices) 
    problem = forms.CharField()
    remarks = forms.CharField()
    atm_issue_priority = forms.ChoiceField(
        choices=CHOICES)    
    
    provide_date = forms.DateField(widget=MyDateInput)
   

    # class Meta:
    #     model = AtmIssueDetails
    #     fields = [
    #         's_n',
    #         'branch_name',
    #         'branch_code',
    #         'atm_terminal_id',
    #         'problem',
    #         'remarks',
    #         'atm_issue_priority'
    #     ]

    
    
