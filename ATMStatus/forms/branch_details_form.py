from ATMStatus.models import BranchDetails
from django import forms


class BranchDetailsForm(forms.Form):

    # class Meta:
    #     model = BranchDetails
    #     fields = ['s_n','branch_name','branch_code']
    s_n = forms.IntegerField()
    branch_name = forms.CharField(max_length=100)
    branch_code = forms.CharField(max_length=3,widget=forms.TextInput(attrs={'placeholder': 'Please provide branch code in number.'}))
    
    def __str__(self):
        return self.branch_name