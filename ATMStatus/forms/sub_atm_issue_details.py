from django import forms


class MyDateInput(forms.DateInput):
    input_type = 'date'


class SubAtmIssueDetailsForm(forms.Form):

    CHOICES = [('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')]
    sub_issue_no = forms.IntegerField()
    problem = forms.CharField()
    remarks = forms.CharField()
    atm_issue_priority = forms.ChoiceField(
        choices=CHOICES)

    provide_date = forms.DateField(widget=MyDateInput)

    # class Meta:
    #     model = AtmIssueDetails
    #     fields = [
    #         's_n',
    #         'branch_name',
    #         'branch_code',
    #         'atm_terminal_id',
    #         'problem',
    #         'remarks',
    #         'atm_issue_priority'
    #     ]
