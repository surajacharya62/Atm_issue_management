from django.contrib import forms
from ATMStatus.models import AtmIssueDetails


class AtmIssueDetailsForm(forms.ModelForm):

    class Meta:
        model = AtmIssueDetails
        fields = [
            's_n',
            'branch_name',
            'branch_code',
            'atm_terminal_id',
            'problem',
            'remarks',
            'atm_issue_priority'
        ]
