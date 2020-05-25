from django.contrib import admin

from . models import (
    AtmDetails,
    AtmTerminalIdDetails,
    AtmIssueDetails,
    BranchDetails,
    ATMLoginCredentialsDetails
)

# Register your models here.


class BranchDetailsAdmin(admin.ModelAdmin):
    list_display = ('s_n', 'branch_name', 'branch_code')


class AtmTerminalDetailsAdmin(admin.ModelAdmin):
    list_display = ('s_n', 'atm_terminal_id')


class AtmDetailsAdmin(admin.ModelAdmin):
    list_display = ('s_n',
                    'branch_name',
                    'branch_code',
                    'atm_location',
                    'atm_terminal_id',
                    'atm_address',
                    'atm_ip_address',
                    'switch_ip_address',
                    'switch_port_number',
                    'atm_installed_date')


class AtmIssueDetailsAdmin(admin.ModelAdmin):
    list_display = (
        's_n',
        'branch_name',
        'branch_code',
        'atm_terminal_id',
        'problem',
        'remarks',
        'atm_issue_priority'
    )


class ATMLoginCredentialsDetailsAdmin(admin.ModelAdmin):
    list_display = (
        's_n',
        'branch_name',
        'branch_code',
        'ATM_IP',
        'VNC_password',
        'R_admin_user_name',
        'R_admin_password',
        'ATM_journal_user_name',
        'ATM_journal_password'


    )


admin.site.register(AtmTerminalIdDetails, AtmTerminalDetailsAdmin)
admin.site.register(AtmDetails, AtmDetailsAdmin)
admin.site.register(AtmIssueDetails, AtmIssueDetailsAdmin)
admin.site.register(BranchDetails, BranchDetailsAdmin)
admin.site.register(ATMLoginCredentialsDetails,
                    ATMLoginCredentialsDetailsAdmin)
