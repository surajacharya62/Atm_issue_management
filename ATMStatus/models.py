from django.db import models


class ViewATMStatus(models.Model):
    s_n = models.IntegerField(null=True)
    branch_name = models.CharField(max_length=100,null=True)
    problem = models.CharField(max_length=2083,null=True)
    remarks = models.CharField(max_length=100,null=True)
    terminal_id = models.CharField(max_length=17,null=True)
    atm_terminal_name = models.CharField(max_length=25,null=True)
    atm_ip_address = models.CharField(max_length=50,null=True)
    switch_ip_address = models.CharField(max_length=50,null=True)
    port_number =  models.IntegerField(null=True)
