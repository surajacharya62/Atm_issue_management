from django.contrib import admin

from . models import ViewATMStatus

# Register your models here.

class ViewATMStatusAdmin(admin.ModelAdmin):
    list_display = ('s_n','branch_name','problem','remarks','terminal_id','atm_terminal_name','atm_ip_address','switch_ip_address','port_number')


admin.site.register(ViewATMStatus,ViewATMStatusAdmin)
