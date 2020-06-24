from django import forms
from django.shortcuts import render
from ATMStatus.models import AtmDetails, BranchDetails
from ATMStatus.sql_operations.sql_operation_atm_details import SqlAtmDetails


class MyDateInput(forms.DateInput):
    input_type = 'date'


class AtmDetailsForm(forms.Form):

    object_sql_atm_details = SqlAtmDetails()
    result_branch_code = object_sql_atm_details.get_all_branch_code()
    result_branch_name = object_sql_atm_details.get_all_branch_name() 
    result_terminal_id =  object_sql_atm_details.get_all_terminal_id() 

    
    branch_code_choices = [(branchCode.id, branchCode.branch_code)
                           for branchCode in result_branch_code]      

    branch_name_choices = [(branchName.branch_name, branchName.branch_name)
                           for branchName in result_branch_name]
    terminal_id_choices = [(TerminalId.id, TerminalId.terminal_id)
                            for TerminalId in result_terminal_id]

    CHOICES = [('OffSite', 'OffSite'), ('OnSite', 'OnSite'), ]
    s_n = forms.IntegerField()
    branch_name = forms.ChoiceField(required=True, choices=[(
        None, 'Please select branch name')]+branch_name_choices)
    branch_code = forms.ChoiceField(required=True, choices=[(
        None, 'Please select branch code')]+branch_code_choices)
    atm_terminal_id = forms.ChoiceField(required=True, choices=[(
        None, 'Please select atm terminal id')]+terminal_id_choices)
    atm_location = forms.ChoiceField(choices=CHOICES)
    atm_address = forms.CharField(max_length=100)
    atm_ip_address = forms.CharField(max_length=12)
    switch_ip_address = forms.CharField(max_length=12)
    switch_port_number = forms.IntegerField()
    atm_installed_date = forms.DateField(widget=MyDateInput)

    # class Meta:
    #     model = AtmDetails
    #     fields = ['id',
    #               's_n',
    #               'branch_name',
    #               'branch_code',
    #               'atm_location',
    #               'atm_terminal_id',
    #               'atm_address',
    #               'atm_ip_address',
    #               'switch_ip_address',
    #               'switch_port_number',
    #               'atm_installed_date']

    
    
    # branch_name = forms.ForeignKey(
    #     BranchDetails, on_delete=models.CASCADE, related_name='AtmDetails_branch_name')
    # branch_code = forms.IntegerField(default='Please choose branch code')
    # atm_terminal_id = forms.ForeignKey(
    #     AtmTerminalIdDetails, on_delete=models.CASCADE, null=True)
 
    # atm_installed_date = forms.DateField()
