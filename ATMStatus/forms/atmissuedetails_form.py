from django import forms
from ATMStatus.models import AtmIssueDetails, BranchDetails


class AtmIssueDetailsForm(forms.ModelForm):

    branch_choices = [(branchCode.branch_code, branchCode.branch_code)
                      for branchCode in BranchDetails.objects.all()]
    branch_code = forms.ChoiceField(required=True, choices=[(
        None, 'Please select branch code')]+branch_choices)

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
