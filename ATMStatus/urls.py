from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('',views.index),
    # path('addatmstatus/',views.add_form_status),
    path('addterminalid/',views.add_terminal_id_details, name="add_terminal_id"),
    path('viewallatmterminalid/',views.view_atm_terminal_id_details, name="view_atm_terminal_id"),
    path('contact/',views.contact, name="ATMStatus_contact"),
    path('<int:pid>/',views.modify_atm_issue,name='modify_atm_issue'),
    path('updateatm/',views.update_atm_issue, name='update_atm_issue'),
    path('deleteatmissue/<int:pid>',views.delete_atm_issue, name='delete_atm_issue')


]