from django import forms
from django.shortcuts import render
from .models import AtmDetails, AtmTerminalIdDetails


class MyDateInput(forms.DateInput):
    input_type = 'date'


class AtmDetailsForm(forms.ModelForm):
    atm_installed_date = forms.DateField(widget=MyDateInput)
    # branch_name = forms.ChoiceField(
    #     choices=[(i.atm_terminal_id, i.atm_terminal_id)
    #              for i in AtmTerminalIdDetails.objects.all()],
    #     required=True)

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
