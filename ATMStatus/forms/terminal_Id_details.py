from django import forms
from ATMStatus.models import AtmTerminalIdDetails


class TerminalIdForm(forms.Form):
    # class Meta:
    #     model = AtmTerminalIdDetails
    #     fields = ['s_n', 'atm_terminal_id']
    s_n = forms.IntegerField()
    atm_terminal_id = forms.CharField(max_length=8)

    def __str__(self):
        return self.atm_terminal_id
