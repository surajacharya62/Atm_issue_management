from django import forms
from .models import ViewATMStatus


class AddATMStatusForm(forms.ModelForm):
    class Meta:
        model = ViewATMStatus
        fields = ['s_n','branch_name','problem','terminal_id','remarks','atm_terminal_name','switch_ip_address','atm_ip_address','port_number']