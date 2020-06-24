from django.db import models

from django.core.validators import RegexValidator, validate_slug


class BranchDetails(models.Model):
    s_n = models.IntegerField()
    branch_name = models.CharField(max_length=100)
    branch_code = models.IntegerField()

    def __str__(self):
        return self.branch_name


class AtmTerminalIdDetails(models.Model):
    s_n = models.IntegerField()
    atm_terminal_id = models.CharField(max_length=8)

    def __str__(self):
        return self.atm_terminal_id


class AtmDetails(models.Model):
    CHOICES = [('OffSite', 'OffSite'), ('OnSite', 'OnSite'), ]
    s_n = models.IntegerField()
    branch_name = models.ForeignKey(
        BranchDetails, on_delete=models.CASCADE, related_name='AtmDetails_branch_name')
    branch_code = models.IntegerField(default='Please choose branch code')
    atm_terminal_id = models.ForeignKey(
        AtmTerminalIdDetails, on_delete=models.CASCADE, null=True)
    atm_location = models.CharField(
        choices=CHOICES, default='OnSite', max_length=7,)
    atm_address = models.CharField(max_length=100, null=True)
    atm_ip_address = models.CharField(max_length=12)
    switch_ip_address = models.CharField(max_length=12)
    switch_port_number = models.IntegerField(default=24023)
    atm_installed_date = models.DateField()


class AtmIssueDetails(models.Model):
    CHOICES = [('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')]
    s_n = models.IntegerField(null=True)
    branch_name = models.ForeignKey(
        BranchDetails, on_delete=models.CASCADE, null=True, related_name='AtmIssuedDetails_branch_name')
    branch_code = models.IntegerField(null=True)
    atm_terminal_id = models.ForeignKey(
        AtmTerminalIdDetails, on_delete=models.CASCADE, null=True)
    problem = models.CharField(max_length=2083, null=True)
    remarks = models.CharField(max_length=2083, null=True)
    atm_issue_priority = models.CharField(
        choices=CHOICES, default='Medium', max_length=6)


class ATMLoginCredentialsDetails(models.Model):
    s_n = models.IntegerField()
    branch_name = models.ForeignKey(
        BranchDetails, on_delete=models.CASCADE, related_name='BranchDetails_branch_name')
    branch_code = models.IntegerField()
    ATM_IP = models.CharField(max_length=50)
    VNC_password = models.CharField(max_length=50, blank=True, default='')
    R_admin_user_name = models.CharField(max_length=50,blank=True, default='' )
    R_admin_password = models.CharField(max_length=50,blank=True, default='')    
    ATM_journal_user_name = models.CharField(max_length=50,blank=True, default='')
    ATM_journal_password = models.CharField(max_length=50,blank=True, default='')
   