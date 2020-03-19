from django import forms
from . models import AtmTerminalIdDetails

class AddTerminalIdForm(forms.ModelForm):
    class Meta:
        model = AtmTerminalIdDetails
        fields = ['s_n','atm_terminal_id']
