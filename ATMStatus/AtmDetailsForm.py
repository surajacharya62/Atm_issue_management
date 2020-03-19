from django import forms
from django.shortcuts import render
from .models import AtmDetails,AtmTerminalIdDetails


class AtmDetailsForm(forms.ModelForm):
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

    # def clean_switch_ip(self,*args,**kwargs):
    #     ip = self.cleaned_data.get('switch_ip_address')
    #     if not "test" in ip:
    #         print("error")
    #         raise forms.ValidationError("Not valid")

    # def clean(self):
    #     cleaned_data = super(AddATMStatusForm, self).clean()
    #     ip = cleaned_data.get('switch_ip_address')
    #     if not "test" in ip:
    #         print("error-Big error")
    #
    #     return ip