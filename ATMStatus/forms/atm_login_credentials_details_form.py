from ATMStatus.models import ATMLoginCredentialsDetails, BranchDetails, AtmDetails
from django import forms


class ATMLoginCredentialsDetailsForm(forms.ModelForm):

    branch_choices = [(branchCode.branch_code, branchCode.branch_code)
                      for branchCode in BranchDetails.objects.all()]
    branch_code = forms.ChoiceField(required=True, choices=[(
        None, 'Please select branch code')]+branch_choices)

    ATM_IP_choices = [(atmip.atm_ip_address, atmip.atm_ip_address)
                      for atmip in AtmDetails.objects.all()]
    ATM_IP = forms.ChoiceField(required=True, choices=[(
        None, 'Please select ATM IP')]+ATM_IP_choices)

   

    class Meta:
        model = ATMLoginCredentialsDetails
        fields = [
            's_n',
            'branch_name',
            'branch_code',
            'ATM_IP',
            'VNC_password',
            'R_admin_user_name',
            'R_admin_password',
            'ATM_journal_user_name',
            'ATM_journal_password'

        ]
