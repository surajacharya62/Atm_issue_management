from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('',views.index),
    url('Addatmstatus/',views.add_form_status),
    path('contact/',views.contact, name="ATMStatus_contact"),
    path('viewatmissue/',views.view_atm_issue, name='view_atm_issue'),
    path('<int:pid>/',views.modify_atm_issue,name='modify_atm_issue'),
    path('<int:pid>/',views.update_atm_issue, name='update_atm_issue'),
    path('deleteatmissue/<int:pid>',views.delete_atm_issue, name='delete_atm_issue')


]