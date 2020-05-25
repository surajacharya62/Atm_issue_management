from django import forms
from django.shortcuts import render
from ATMStatus.models import AtmDetails, BranchDetails


class MyDateInput(forms.DateInput):
    input_type = 'date'


class AtmDetailsForm(forms.ModelForm):
    atm_installed_date = forms.DateField(widget=MyDateInput)
    branch_choices = [(branchCode.branch_code, branchCode.branch_code)
                      for branchCode in BranchDetails.objects.all()]
    branch_code = forms.ChoiceField(required=True, choices=[(
        None, 'Please select branch code')]+branch_choices)

    class Meta:
        model = AtmDetails
        fields = ['id',
                  's_n',
                  'branch_name',
                  'branch_code',
                  'atm_location',
                  'atm_terminal_id',
                  'atm_address',
                  'atm_ip_address',
                  'switch_ip_address',
                  'switch_port_number',
                  'atm_installed_date']
