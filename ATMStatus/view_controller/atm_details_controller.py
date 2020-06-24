from ViewATMStatus.db_connection_string import connection_string
from django.shortcuts import render, redirect
from django.contrib import messages
from ATMStatus.sql_operations.sql_operation_atm_details import SqlAtmDetails
import re

class AtmDetailsController:

    def view_controller(self,request):
            pass
       
           