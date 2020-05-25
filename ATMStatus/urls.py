from django.urls import path
from django.conf.urls import url
from ATMStatus import views
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static
from .views import AtmDetailsListView, AtmIssueDetailsListView, AtmLoginCredentialsDetailsListView, terminalAPIClass


urlpatterns = [

    path('', views.view_atm_terminal_id_details,
         name="view_all_atm_terminal_id_details"),
    path('api/', views.serialize, name='api-test1'),
    path('api/<int:pk>/', views.terminal_serialize, name='api-test2'),
    path('apiclass/', terminalAPIClass.as_view(), name='apiclass'),
    path('addterminalid/', views.add_terminal_id_details, name="add_terminal_id"),
    path('viewallatmterminalid/', views.view_atm_terminal_id_details,
         name="ATMStatus_view_atm_terminal_id"),
    path('modifyatmterminalid/<int:pid>/', views.modify_atm_terminal_id,
         name='ATMStatus_modify_terminal_id'),
    path('deleteatmterminalid/<int:pid>/', views.delete_atm_terminal_id,
         name='ATMStatus_delete_terminal_id'),
    path('addatmdetails/', views.add_atm_details, name="add-atm-details"),
    path('editatmdetails/<int:pid>/',
         views.modify_atm_details, name="modify-atm-details"),
    path('deleteatmdetails/<int:pid>/',
         views.delete_atm_details, name="delete-atm-details"),
    path('viewallatmdetails/', AtmDetailsListView.as_view(),
         name="view-all-atm-details"),
    path('addatmissuedetails/', views.add_atm_issue_details,
         name="add-atm-issue-details"),
    path('modifyatmissuedetails/<int:pid>/', views.modify_atm_issue_details,
         name="modify-atm-issue-details"),
    path('deleteatmissuedetails/<int:pid>/', views.delete_atm_issue_details,
         name="delete-atm-issue-details"),
    path('viewallatmissuedetails/', AtmIssueDetailsListView.as_view(),
         name="view-atm-issue-details"),
    path('viewalllogincredentialsdetails/', AtmLoginCredentialsDetailsListView.as_view(),
         name='view-atm-login-credentials-details'),
    path('addatmlogincredentialsdetails/', views.add_atm_login_credentials_details,
         name='add-atm-login-credentials-details'),
    path('modifyatmlogincredentialsdetails/<int:pid>/', views.modify_atm_login_credentials_details,
         name='modify-atm-login-credentials-details'),
    path('exporttoexcel/', views.export_to_excel, name='export-excel')

]
