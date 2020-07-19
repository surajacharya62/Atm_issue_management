from ATMStatus.models import ATMLoginCredentialsDetails, BranchDetails, AtmDetails
from django import forms
from ATMStatus.sql_operations.sql_operation_login_crendential_details import SqlLoginCredentialdetails


class ATMLoginCredentialsDetailsForm(forms.Form):

    s_n = forms.IntegerField()
    branch_code = forms.ChoiceField(
        required=True, choices=[])
    ATM_IP = forms.ChoiceField(required=True, choices=[])
    VNC_password = forms.CharField(max_length=50, required=False)
    R_admin_user_name = forms.CharField(
        max_length=50, required=False)
    R_admin_password = forms.CharField(max_length=50, required=False)
    ATM_journal_user_name = forms.CharField(
        max_length=50, required=False)
    ATM_journal_password = forms.CharField(
        max_length=50, required=False)

    def __init__(self, *args, **kwargs):
        object_login_details = SqlLoginCredentialdetails()
        super(ATMLoginCredentialsDetailsForm, self).__init__(*args, **kwargs)
        result_branch_code = object_login_details.get_all_branch_code()

        result_atm_ip = object_login_details.get_all_atm_ip()

        self.fields['branch_code'] = forms.ChoiceField(required=True, choices=[(None, 'Please select branch code')]+[(branchcode.id, branchcode.branch_code)
                                                                                                                     for branchcode in result_branch_code])
        self.fields['ATM_IP'] = forms.ChoiceField(required=True, choices=[(None, 'Please select atm ip')]+[(atmip.atm_ip_address, atmip.atm_ip_address)
                                                                                                           for atmip in result_atm_ip])
        # branch_code = forms.ChoiceField(required=True, choices=[(
    #                                 None, "Please provide branch code")]+branch_code_choices)

    # ATM_IP = forms.ChoiceField(required=True, choices=[(
    #                            None, "Please select atm ip")]+atm_ip_choices)
    # branch_choices = [(branchCode.branch_code, branchCode.branch_code)
    #                   for branchCode in BranchDetails.objects.all()]
    # branch_code = forms.ChoiceField(required=True, choices=[(
    #     None, 'Please select branch code')]+branch_choices)

    # ATM_IP_choices = [(atmip.atm_ip_address, atmip.atm_ip_address)
    #                   for atmip in AtmDetails.objects.all()]
    # ATM_IP = forms.ChoiceField(required=True, choices=[(
    #     None, 'Please select ATM IP')]+ATM_IP_choices)

    # class Meta:
    #     model = ATMLoginCredentialsDetails
    #     fields = [
    #         's_n',
    #         'branch_name',
    #         'branch_code',
    #         'ATM_IP',
    #         'VNC_password',
    #         'R_admin_user_name',
    #         'R_admin_password',
    #         'ATM_journal_user_name',
    #         'ATM_journal_password'

    #     ]

    s_n = forms.IntegerField()
    VNC_password = forms.CharField(max_length=50, required=False)
    R_admin_user_name = forms.CharField(
        max_length=50, required=False)
    R_admin_password = forms.CharField(max_length=50, required=False)
    ATM_journal_user_name = forms.CharField(
        max_length=50, required=False)
    ATM_journal_password = forms.CharField(
        max_length=50, required=False)
