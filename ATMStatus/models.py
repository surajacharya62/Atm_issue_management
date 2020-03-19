from django.db import models
from .validators import validate_switch_ip
from django.core.validators import RegexValidator, validate_slug


class AtmTerminalIdDetails(models.Model):
    s_n = models.IntegerField()
    atm_terminal_id = models.CharField(max_length=8)


class AtmDetails(models.Model):
    CHOICES = [('OffSite','OffSite'),('OnSite','OnSite')]
    s_n = models.IntegerField()
    branch_name = models.CharField(max_length=100)
    branch_code = models.IntegerField()
    atm_terminal_id = models.ForeignKey(AtmTerminalIdDetails, on_delete=models.CASCADE, null=True)
    atm_location = models.CharField(choices= CHOICES, default='OnSite',max_length=7,)
    atm_address = models.CharField(max_length=100, null= True)
    atm_ip_address = models.CharField(max_length=12)
    switch_ip_address = models.CharField(max_length=12)
    switch_port_number = models.IntegerField(default=24023)
    atm_installed_date = models.DateField()


class AtmIssueDetails(models.Model):
    s_n = models.IntegerField(null=True)
    branch_name = models.ForeignKey(AtmDetails,on_delete=models.CASCADE, null=True)
    branch_code = models.ForeignKey(AtmDetails,on_delete=models.CASCADE, null=True)
    atm_terminal_id = models.ForeignKey(AtmTerminalIdDetails,on_delete=models.CASCADE, null=True)
    problem = models.CharField(max_length=2083,null=True)
    remarks = models.CharField(max_length=2083,null=True)
    atm_issue_priority = models.CharField(choices=['High','Medium','Low'],default='Medium',max_length=6)



