from django.contrib import admin

from . models import AtmDetails,AtmTerminalIdDetails,AtmIssueDetails

# Register your models here.


class AtmTerminalDetailsAdmin(admin.ModelAdmin):
    list_display = ('s_n','atm_terminal_id')


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
    list_display = ('s_n',
                    'branch_code',
                    'atm_terminal_id',
                    'problem',
                    'remarks',
                    'atm_issue_priority'
                    )


admin.site.register(AtmTerminalIdDetails,AtmTerminalDetailsAdmin)
admin.site.register(AtmDetails,AtmDetailsAdmin)
admin.site.register(AtmIssueDetails,AtmIssueDetailsAdmin)
