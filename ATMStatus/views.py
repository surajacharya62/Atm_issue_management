from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework.parsers import JSONParser
from .models import(
    AtmDetails,
    AtmTerminalIdDetails,
    AtmIssueDetails,
    ATMLoginCredentialsDetails,
    BranchDetails)
from ATMStatus.forms.AtmDetailsForm import AtmDetailsForm
from ATMStatus.forms.terminal_Id_details import TerminalIdForm
from ATMStatus.forms.atm_issue_details_form import AtmIssueDetailsForm
from ATMStatus.forms.atm_login_credentials_details_form import ATMLoginCredentialsDetailsForm
from ATMStatus.forms.branch_details_form import BranchDetailsForm
from django.urls import reverse
from django.contrib import messages
import re
from django.views.generic import (
    CreateView, DeleteView, ListView
)
import xlwt
import os
from .serializers import AtmTerminalIdDetailsSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ViewATMStatus import db_connection_string
from ATMStatus.sql_operations import sql_operation_branch_details
from ATMStatus.sql_operations.sq_operation_terminal_id_details import SqlTerminalIdDetails
from ATMStatus.properties.terminal_id_details_properties import TerminalIdDetailsProperties
from ATMStatus.sql_operations.sql_operation_atm_details import SqlAtmDetails
from ATMStatus.view_controller.atm_details_controller import AtmDetailsController
from ATMStatus.sql_operations.sql_operation_atm_issue_details import SqlAtmIssueDetails


def index(request):
    atm_fields = AtmIssueDetails.objects.all()

    return render(request, 'View_ATM_Status.html', {'atm_fields': atm_fields})

'''
    View all all terminal id details.
    Search particular branch details.
'''
def view_atm_terminal_id_details(request):

    try:
        # all_atm_terminal_id = AtmTerminalIdDetails.objects.all()
        all_atm_terminal_id = ''
        result = ''
        if request.method == 'POST':
            search_value =  request.POST.get("search_text")
            atm_id_pattern = re.compile('JBBL[0-9][0-9][0-9]')
            object_terminal_properties = TerminalIdDetailsProperties()
            object_terminal_properties.terminal_id_setter(search_value) 
            object_particular_terminal = SqlTerminalIdDetails()
            result  = object_particular_terminal.get_particular_terminal_id_details(object_terminal_properties)
           

            if not atm_id_pattern.match(search_value):
                messages.warning(
                    request, f'Please follow the [JBBL_branchid_01]')           
            else:                
                 
               
                try:
                    if result:                        
                       
                        return render(request, 'ATMStatus/atm_terminal_details/view_atm_terminal_id_details.html', {'all_atm_terminal_id': result})
                    
                except:
                    messages.error(request,f'Could not load particular data')
                
                finally:                    
                    result.close()
        else:
            object_terminal = SqlTerminalIdDetails()
            result = object_terminal.view_all_terminal_id_details()
            try:
                if result:
                    all_atm_terminal_id = result
                    print(all_atm_terminal_id)
                    return render(request, 'ATMStatus/atm_terminal_details/view_atm_terminal_id_details.html', {'all_atm_terminal_id': all_atm_terminal_id})
              
            except:
                messages.error(request,f'No datas are found.')
                
            finally:
                result.close()
         
    except:
        messages.error(request,f'Something went wrong')
    
    return render(request, 'ATMStatus/atm_terminal_details/view_atm_terminal_id_details.html', {'all_atm_terminal_id': all_atm_terminal_id})
   

'''
    Add new terminal id details.
'''  
def add_terminal_id_details(request):
    try:
        object_sql_terminal_id = SqlTerminalIdDetails()
        add_terminal_id = TerminalIdForm()
        if request.method == "POST":
            add_terminal_id = TerminalIdForm(request.POST)
            if add_terminal_id.is_valid():
                s_n = add_terminal_id.cleaned_data.get('s_n')
                atm_id = add_terminal_id.cleaned_data.get('atm_terminal_id')

                object_terminal_id_properties = TerminalIdDetailsProperties()
                        
                object_terminal_id_properties.s_n_setter(s_n)
                object_terminal_id_properties.terminal_id_setter(atm_id)                
                
                # is_terminal_id_already_exist = AtmTerminalIdDetails.objects.filter(
                # atm_terminal_id=atm_id).values('id')

                is_terminal_id_already_exist = object_sql_terminal_id.get_particular_terminal_id_details(object_terminal_id_properties)
                
                atm_id_pattern = re.compile('JBBL[0-9][0-9][0-9]')

                if is_terminal_id_already_exist:
                    messages.warning(
                        request, f'Your provided terminal id is already exists.')
                elif not atm_id_pattern.match(atm_id):
                    
                    # error_message = 'Please follow the [JBBL_branchid_01]' 
                    messages.warning(
                        request, f'Please follow the [JBBL_branch_id]-(ex: JBBL001)')
                else:
                    result = object_sql_terminal_id.add_terminal_id_details(object_terminal_id_properties)
                    print(result)
                    try:

                        if result:
                            result.commit()
                            messages.success(
                                request, 'New ATM terminal has been added successfully.')
                            # add_terminal_id.save()
                            return redirect(view_atm_terminal_id_details)
                    except:
                        messages.warning(                    
                        request, f'Could not insert data.')   
                    finally:
                        result.close()
                        
            
        else:
            
            total_row = object_sql_terminal_id.total_row_count()
            total_row += 1
            add_terminal_id.fields['s_n'].initial = total_row
            add_terminal_id.fields['s_n'].widget.attrs['readonly'] = True

    except:
        messages.warning(                    
                    request, f'Something went wrong.')  
    return render(request, 'ATMStatus/atm_terminal_details/add_terminal_id_details.html', {'add_terminal_id': add_terminal_id})


'''
    Modify particular atm terminal details.
'''
def modify_atm_terminal_id(request, pid):
    # update_terminal_id = AtmTerminalIdDetails.objects.get(id=pid)
    # previous_atm_id = update_terminal_id.atm_terminal_id   
    try:
        query_result = ''
        previous_terminal_id = ''

        object_sql_terminal =  SqlTerminalIdDetails()
        query_result = object_sql_terminal.get_update_data(pid) 
        
        for value in query_result:
            previous_terminal_id = value[2]

        form = TerminalIdForm()

        modify_atm_terminal_id = ''
        if request.method == "POST":
            # modify_atm_terminal_id = AddTerminalIdForm(
            #     request.POST, instance=update_terminal_id)

            form = TerminalIdForm(request.POST)        

            if form.is_valid():

                post_s_n = form.cleaned_data.get('s_n')
                post_terminal_id = form.cleaned_data.get('atm_terminal_id')

                # new_atm_id = modify_atm_terminal_id.cleaned_data.get(
                #     'atm_terminal_id')
                terminal_id_properties = TerminalIdDetailsProperties()
                terminal_id_properties.s_n_setter(post_s_n)
                terminal_id_properties.terminal_id_setter(post_terminal_id)

                query_result = object_sql_terminal.update_terminal_id_details(terminal_id_properties,pid)

                atm_id_pattern = re.compile('JBBL[0-9][0-9][0-9]')

                if not atm_id_pattern.match(post_terminal_id):

                    # error_message = 'Please follow the [JBBL_branchid_01]'
                    messages.warning(
                        request, f'Please follow the [JBBL_branch_id]-(ex: JBBL001)')
                else:
                    try:
                        if query_result:
                            query_result.commit()
                            messages.success(
                                request, f"ATM ID '{previous_terminal_id }' has been successfully modified to '{post_terminal_id}'")
                            # modify_atm_terminal_id.save()
                            return redirect(view_atm_terminal_id_details)
                    except:
                        messages.warning(
                        request, f'Could not update data.')
                    finally:
                        query_result.close()
            
        else:
            # modify_atm_terminal_id = AddTerminalIdForm(instance=update_terminal_id)
            # total_row = AtmTerminalIdDetails.objects.all().count()
            # total_row = 
            # total_row += 1 
            # modify_atm_terminal_id.fields['s_n'].initial = total_row
            
            
            for value in query_result:                  
                form.fields['s_n'].initial = value[1]
                form.fields['s_n'].widget.attrs['readonly'] = True
                form.fields['atm_terminal_id'].initial = value[2]    
    except:
          messages.warning(
                        request, f'Something went wrong.')

    return render(request, 'ATMStatus/atm_terminal_details/modify_atm_terminal_id_details.html', {'modify_atm_terminal_id': form})

'''
    Delete terminal id details.
'''
def delete_atm_terminal_id(request, pid):

    
    object_terminal_id = SqlTerminalIdDetails()
    query_result = object_terminal_id.get_particular_terminal_id_details('default',pid)
    # delete_terminal_id = AtmTerminalIdDetails.objects.get(id=pid)
    # deleted_atm_id = delete_terminal_id.atm_terminal_id
    delete_terminal_id = query_result
    if request.method == "POST":
        query_result = object_terminal_id.delete_terminal_id_details(pid)

        if query_result:            
            query_result.commit()
            messages.success(
                request, f"Temrinal ID '{delete_terminal_id}' details have been successfully deleted.")
            # delete_terminal_id.delete()
            return redirect(view_atm_terminal_id_details)
    
    return render(request, 'ATMStatus/atm_terminal_details/delete_atm_terminal_id_details.html', {'delete_atm_id': delete_terminal_id})


# class ATMTerminalIdDetailsDeleteView(DeleteView):
#     model = AtmTerminalIdDetails
#     success_url = '/ATMStatus/viewallatmterminalid'

'''
    View all atm details.
'''
def view_atm_details(request):
    query_result = ''

    if request.method == 'POST':
        search_value = request.POST.get('search_text')

        object_sql_atm_details = SqlAtmDetails()
                      
            
        branch_code_pattern = re.compile('[0-9][0-9][0-9]')

        if not int(search_value) > 0:
            messages.warning(
                request, f'Please provide valid branch code.')
        elif len(search_value) > 3:
            messages.warning(
                request, f'Please follow branch code pattern[000] that it should not exceed than 3.')

        elif not branch_code_pattern.match(str(search_value)):
            messages.warning(
                request, f'Please follow branch code pattern-(010).')
        else:
            try:
                query_result = object_sql_atm_details.sql_get_particular_atm_details(search_value) 
              
                if query_result:                                                         
                    return render(request,'ATMStatus/atm_details/view_atm_details.html',{'all_atm_details':query_result}) 
                else:
                    messages.warning(request,'Could not load particular details.')  
            except:
                    messages.warning(request,'Could not load particular details.')               
            finally:
                query_result.close() 
    
    else:            
        object_sql_atm_details  = SqlAtmDetails()
        query_result = object_sql_atm_details.sql_view_atm_details()        
        
        try:
            if query_result: 
                return render(request,'ATMStatus/atm_details/view_atm_details.html',{'all_atm_details':query_result}) 
        except:
                messages.error(request,'No data found.')
        finally:
            query_result.close()

    return render(request,'ATMStatus/atm_details/view_atm_details.html',{'all_atm_details':query_result})


# class AtmDetailsListView(ListView):
#     all_atm_details = AtmDetails.objects.all()
#     model = AtmDetails
#     template_name = 'ATMStatus/atm_details/view_atm_details.html'
#     context_object_name = 'all_atm_details'
#     paginate_by = 10


def add_atm_details(request):
    try:
        form = AtmDetailsForm()
        object_atm_details = SqlAtmDetails()
        
        # total_row = AtmDetails.objects.all().count()
        # try:
        if request.method == 'POST':
            form = AtmDetailsForm(request.POST)
            if form.is_valid():
                object_atm_details.s_n =  form.cleaned_data.get('s_n')
                object_atm_details.branch_name = form.cleaned_data.get('branch_name')
                object_atm_details.branch_code = form.cleaned_data.get('branch_code')
                object_atm_details.atm_terminal_id = form.cleaned_data.get('atm_terminal_id')           
                object_atm_details.atm_location =  form.cleaned_data.get('atm_location')
                object_atm_details.atm_address =  form.cleaned_data.get('atm_address')
                object_atm_details.atm_ip_address = form.cleaned_data.get(
                        'atm_ip_address') 
                object_atm_details.switch_ip_address = form.cleaned_data.get(
                        'switch_ip_address')
                object_atm_details.switch_port_number =  form.cleaned_data.get('switch_port_number')      
                    
                object_atm_details.atm_installed_date = form.cleaned_data.get(
                        'atm_installed_date')
                
        
                is_branch_name_already_exists = object_atm_details.get_branch_name(object_atm_details.branch_name)
                is_branch_code_already_exists = object_atm_details.get_branch_code(object_atm_details.branch_code)
                is_terminal_id_already_exists = object_atm_details.get_terminal_id(object_atm_details.atm_terminal_id)
                
                # print(is_branch_name_exists,is_branch_code_exists)
                
                # print(object_atm_details.branch_code,object_atm_details.atm_terminal_id,is_details_already_exists)

                # test = AtmDetails.objects.values_list(
                #     'id').get(branch_name=valid_branch_name)

                # is_branchname_already_exists = AtmDetails.objects.filter(
                #     branch_name=branch_name).values('id')

                pattern = re.compile('10[.][0-9][0-9][.][0-9][0-9]')

                if is_branch_name_already_exists:
                    messages.warning(
                        request, f'Your provided branch name is already exists.')
                elif is_branch_code_already_exists:
                    messages.warning(
                        request, f'Your provided branch code is already exists with other branch details.')
                elif is_terminal_id_already_exists:
                    messages.warning(
                        request, f'Your provided terminal ID is already exists with other branch details.')
                elif not pattern.match(object_atm_details.atm_ip_address):
                    messages.warning(
                        request, f'Please follow the [10.00.00.00] pattern in "ATM IP Address."')
                elif not pattern.match(object_atm_details.switch_ip_address):
                    messages.warning(
                        request, f'Please follow the [10.00.00.00] pattern in "Switch IP Address."')
                else:
                    query_result = object_atm_details.add_atm_details(object_atm_details)
                    try:
                        if query_result:
                            query_result.commit()
                            return redirect('view-all-atm-details')
                    except:
                        messages.warning(
                        request, f'Could not add atm details.')
                    finally:
                        query_result.close()

        else:

            try:
                total_row = object_atm_details.get_row_count_atm_details()
                for row in total_row:
                    total_count = row[0]
                form.fields['s_n'].initial = total_count + 1
                form.fields['s_n'].widget.attrs['readonly'] = True
                form.fields['switch_port_number'].initial = 24023
                form.fields['switch_port_number'].widget.attrs['readonly'] = True
            except:
                messages.warning(
                request, f'Unable to load s_n number')
            finally:
                total_row.close()
    except:
        messages.warning(
            request, f'Something went wrong in input data.')

    form.fields['s_n'].widget.attrs['readonly'] = True
    form.fields['switch_port_number'].widget.attrs['readonly'] = True
    return render(request, 'ATMStatus/atm_details/add_atm_details.html', {'form': form})


'''
     Update particular atm details.
'''
def modify_atm_details(request, pid):

    object_atm_details = SqlAtmDetails()
    result = object_atm_details.get_data_for_update_atm_details(pid)
    # atm_details = AtmDetails.objects.get(id=pid)
    form = AtmDetailsForm()
    
    try:
        if request.method == 'POST':
            form = AtmDetailsForm(request.POST)
            if form.is_valid():

                object_atm_details.s_n =  form.cleaned_data.get('s_n')
                object_atm_details.branch_name = form.cleaned_data.get('branch_name')
                object_atm_details.branch_code = form.cleaned_data.get('branch_code')
                object_atm_details.atm_terminal_id = form.cleaned_data.get('atm_terminal_id')           
                object_atm_details.atm_location =  form.cleaned_data.get('atm_location')
                object_atm_details.atm_address =  form.cleaned_data.get('atm_address')
                object_atm_details.atm_ip_address = form.cleaned_data.get(
                        'atm_ip_address') 
                object_atm_details.switch_ip_address = form.cleaned_data.get(
                        'switch_ip_address')
                object_atm_details.switch_port_number =  form.cleaned_data.get('switch_port_number')     
                    
                object_atm_details.atm_installed_date = form.cleaned_data.get(
                        'atm_installed_date')
                # is_valid_atm_ip_address = form.cleaned_data.get(
                #     'atm_ip_address')
                # is_valid_switch_ip_address = form.cleaned_data.get(
                #     'switch_ip_address')
                # is_valid_branch_name = form.cleaned_data.get('branch_name')

                pattern = re.compile('10[.][0-9][0-9][.][0-9][0-9]')

                if not pattern.match( object_atm_details.atm_ip_address):
                    messages.warning(
                        request, f'Please follow the [10.00.00.00] pattern in ATM IP Address')
                   
                elif not pattern.match(object_atm_details.switch_ip_address):
                    messages.warning(
                        request, f'Please follow the [10.00.00.00] pattern in Switch IP Address')
                   
                else:

                    query_result = object_atm_details.modify_data_atm_details(object_atm_details,pid)
                    try:
                        if query_result:
                            query_result.commit()
                            return redirect('view-all-atm-details')
                    except:
                        messages.warning(
                        request, f'Please follow the [10.00.00.00] pattern in Switch IP Address')
                    finally:
                        query_result.close()           
                     

        else:
            try:

                for row in result:
                    form.fields['s_n'].initial = row[1]
                    form.fields['s_n'].widget.attrs['readonly'] = True
                    form.fields['branch_name'].initial = row[2]
                    form.fields['branch_code'].initial = row[3]
                    form.fields['atm_terminal_id'].initial = row[4]
                    form.fields['atm_location'].initial = row[5]
                    form.fields['atm_address'].initial = row[6]
                    form.fields['atm_ip_address'].initial = row[7]
                    form.fields['switch_ip_address'].initial = row[8]
                    form.fields['switch_port_number'].initial = row[9]
                    form.fields['atm_installed_date'].initial = row[10]
                    form.fields['switch_port_number'].widget.attrs['readonly'] = True
            except:
                messages.warning(
                        request, f'Could not load data.')
            finally:
                result.close()
                    
                
    except:
        pass
        messages.warning(
            request, f'Something went wrong in input data.')
    
    form.fields['s_n'].widget.attrs['readonly'] = True       
    form.fields['switch_port_number'].widget.attrs['readonly'] = True
    return render(request, 'ATMStatus/atm_details/modify_atm_details.html', {'form': form})

'''
    Delete particular atm details
'''

def delete_atm_details(request, pid):
    
    object_atm_details = SqlAtmDetails()
    delete_atm_details = object_atm_details.view_branchname_for_delete(pid)
    # delete_atm_details = AtmDetails.objects.get(id=pid)
    if request.method == 'POST':
        query_result = object_atm_details.delete_atm_details(pid)
        # delete_atm_details.delete()
        
        try:
            if query_result:
                query_result.commit()
                messages.success(
                    request, f"'{delete_atm_details}' ATM details has been successfully deleted!")
                return redirect('view-all-atm-details')
        except:
            messages.warning(request, f" Unable to delete '{delete_atm_details}' ATM details.")
                

    return render(request, 'ATMStatus/atm_details/delete_atm_details.html', {'delete_atm_details': delete_atm_details})


class AtmIssueDetailsListView(ListView):
    all_atm_issue_details = AtmIssueDetails.objects.all()
    model = AtmIssueDetails   
    template_name = 'ATMStatus/atm_issue_details/view_atm_issue_details.html'
    context_object_name = 'all_atm_issue_details'
    paginate_by = 10


'''
    View all atm issue details.
'''
def view_atm_issue_details(request):
    object_sql_issue_details = SqlAtmIssueDetails()
    result = object_sql_issue_details.view_all_issue_details()

    if request.method == 'POST':
        search_value = request.POST.get('search_text')
        result = object_sql_issue_details.get_particular_issue_details(search_value)
 

        try:
            if result:
                return render(request,'ATMStatus/atm_issue_details/view_atm_Issue_details.html',{'all_atm_issue_details':result})
   
        except:
            messages.warning(request, f" Could not load particular data.")           
        finally:
            result.close()
    else:

        try:
            if result:
                return render(request,'ATMStatus/atm_issue_details/view_atm_Issue_details.html',{'all_atm_issue_details':result})
   
        except:
            messages.warning(request, f" Could not load data.")
           
        finally:
            result.close()

    return render(request,'ATMStatus/atm_issue_details/view_atm_Issue_details.html',{'all_atm_issue_details':result})
       

'''
    # -> Adding atm issue details
'''      

def add_atm_issue_details(request):
    try:
        form = AtmIssueDetailsForm()
        object_sql_issue_details = SqlAtmIssueDetails()
        
        # total_row = AtmIssueDetails.objects.all().count()
        
        if request.method == 'POST':
            form = AtmIssueDetailsForm(request.POST)
            if form.is_valid():

                object_sql_issue_details.s_n = form.cleaned_data.get('s_n')
                object_sql_issue_details.branch_code = form.cleaned_data.get('branch_code')
                object_sql_issue_details.terminal_id = form.cleaned_data.get('terminal_id')
                object_sql_issue_details.problem = form.cleaned_data.get('problem')
                object_sql_issue_details.remarks = form.cleaned_data.get('remarks')
                object_sql_issue_details.atm_issue_priority = form.cleaned_data.get('atm_issue_priority')
                object_sql_issue_details.issue_date = form.cleaned_data.get('provide_date')

                result = object_sql_issue_details.add_atm_issue_details(object_sql_issue_details)

                try:
                    if result:
                        result.commit()
                        messages.success(
                            request, f"ATM issue details has been successfully added!")
                        return redirect('view-atm-issue-details')
                except:
                    messages.warning(
                            request, f"Unable to add the data.")
                
                finally:
                    result.close()

            
                    
        else:
            result = object_sql_issue_details.get_total_row_count()
            
            try:
                if result:
                    for row in result:
                        total_row = row[0]
                    form.fields['s_n'].initial = total_row + 1
                    form.fields['s_n'].widget.attrs['readonly'] = True
            except:
                pass
            finally:
                result.close()

    except:
        messages.warning(
            request, f'Something went wrong in input data.')
    form.fields['s_n'].widget.attrs['readonly'] = True
    return render(request, 'ATMStatus/atm_issue_details/add_atm_issue_details.html', {'form': form})

 # -> Adding atm issue details


def modify_atm_issue_details(request, pid):
    object_sql_issue_details = SqlAtmIssueDetails()
    result = object_sql_issue_details.get_data_for_update(pid)
    # update_atm_issue = AtmIssueDetails.objects.get(id=pid)
    form = AtmIssueDetailsForm()
    # try:
    if request.method == 'POST':
        form = AtmIssueDetailsForm(request.POST)
        print('test1')
        if form.is_valid():
            # form.save()
            print('test2')
            object_sql_issue_details.s_n = form.cleaned_data.get('s_n')
            object_sql_issue_details.branch_code = form.cleaned_data.get('branch_code')
            object_sql_issue_details.terminal_id = form.cleaned_data.get('terminal_id')
            object_sql_issue_details.problem = form.cleaned_data.get('problem')
            object_sql_issue_details.remarks = form.cleaned_data.get('remarks')
            object_sql_issue_details.atm_issue_priority = form.cleaned_data.get('atm_issue_priority')
            object_sql_issue_details.issue_date = form.cleaned_data.get('provide_date')
            
            result = object_sql_issue_details.update_atm_issue_details(object_sql_issue_details,pid)
            
            try:
                if result:
                    result.commit()
                    messages.success(
                        request, f" S.N '{object_sql_issue_details.s_n}'  ATM issue details have been successfully modified.")
                    return redirect('view-atm-issue-details')
            except:
                messages.success(
                        request, f" ATM issue details related to the branch code  have been successfully modified!")
            finally:
                result.close()      
    else:
        try:
      
            if result:
                for row in result:
                
                    form.fields['s_n'].initial = row[1]
                    form.fields['s_n'].widget.attrs['readonly']= True
                    form.fields['branch_code'].initial = row[2]
                    form.fields['terminal_id'].initial = row[3] 
                    form.fields['problem'].initial = row[4]
                    form.fields['remarks'].initial = row[5]
                    form.fields['atm_issue_priority'].initial = row[6]
                    form.fields['provide_date'].initial = row[7]
        except:
             messages.success(
                request, f" Could not load data for update.")
        finally:
            result.close()
           
    # except:
    #     messages.warning(
    #         request, f'Something went wrong')

    return render(request, 'ATMStatus/atm_issue_details/modify_atm_issue_details.html', {'form': form})


# ->Deleting the issue details


def delete_atm_issue_details(request, pid):
    delete_atm_issue_details = AtmIssueDetails.objects.get(id=pid)
    if request.method == 'POST':
        messages.success(
            request, f" ATM issue having '{delete_atm_issue_details.id}' ID details has been successfully deleted!")
        delete_atm_issue_details.delete()
        return redirect('view-atm-issue-details')

    return render(request, 'ATMStatus/atm_issue_details/delete_atm_issue_details.html', {'delete_atm_issue_details': delete_atm_issue_details})


class AtmLoginCredentialsDetailsListView(ListView):
    all_atm_login_details = ATMLoginCredentialsDetails.objects.all()
    model = ATMLoginCredentialsDetails
    context = {
        'atmlogindetails': all_atm_login_details

    }
    template_name = 'ATMStatus/atm_login_credentials_details/view_atm_login_credentials_details.html'
    context_object_name = 'context'
    ordering = ['s_n']
    paginate_by = 5


def add_atm_login_credentials_details(request):
    form = ATMLoginCredentialsDetailsForm()
    total_row = ATMLoginCredentialsDetails.objects.all().count()
    # try:
    if request.method == 'POST':
        form = ATMLoginCredentialsDetailsForm(request.POST)
        if form.is_valid():
            atm_branch_name = form.cleaned_data.get('branch_name')
            atm_branch_code = form.cleaned_data.get('branch_code')
            is_branch_name_already_exists = ATMLoginCredentialsDetails.objects.filter(
                branch_name=atm_branch_name).values('id')
            is_branch_code_already_exists = ATMLoginCredentialsDetails.objects.filter(
                branch_code=atm_branch_code).values('branch_code')
            print(is_branch_code_already_exists)
            if is_branch_name_already_exists:
                messages.warning(
                    request, f'Your provided branch name is already exists.')
            elif is_branch_code_already_exists:
                 messages.warning(
                    request, f'Your provided branch code is already exists.')
            else:
                form.save()
                messages.success(
                    request, f"ATM login credentials details have been successfully added!")
                return redirect('view-atm-login-credentials-details')

    else:

        form.fields['s_n'].initial = total_row + 1
        form.fields['s_n'].widget.attrs['readonly'] = True

    # except:
    #     messages.warning(
    #         request, f'Something went wrong')

    return render(request, 'ATMStatus/atm_login_credentials_details/add_atm_login_credentials_details.html', {'form': form})

# -> Modify and update the atm login credentials details


def modify_atm_login_credentials_details(request, pid):

    update_atm_credentials = ATMLoginCredentialsDetails.objects.get(id=pid)
    form = ATMLoginCredentialsDetailsForm(instance=update_atm_credentials)
    atm_branch_name = ATMLoginCredentialsDetails.objects.get(id=pid)
    atm_branch_name_ = atm_branch_name.branch_name    
    atm_branch_code = ATMLoginCredentialsDetails.objects.get(id=pid)
    branch_code =atm_branch_code.branch_code
    atm_IP = ATMLoginCredentialsDetails.objects.get(id=pid)
    get_atm_IP= atm_IP.ATM_IP
    
    try:
        if request.method == 'POST':
            form = ATMLoginCredentialsDetailsForm(
                request.POST, instance=update_atm_credentials)
            if form.is_valid():
                post_branch_code= form.cleaned_data.get('branch_code')
                post_branch_name= form.cleaned_data.get('branch_name')
                post_ATM_IP= form.cleaned_data.get('ATM_IP')
               
                    
                if atm_branch_name_ != post_branch_name:
                    messages.warning(
                    request, f'Branch name should not be altered.')
                elif str(branch_code) != post_branch_code:
                    messages.warning(
                    request, f'Branch code should not be altered.')
                
                elif get_atm_IP !=post_ATM_IP:
                    messages.warning(
                    request, f'ATM IP should not be altered.')
                else:
                    form.save()
                    messages.success(
                    request, f"ID '{update_atm_credentials.id}' ATM login credentials details has been successfully updated!")
                    return redirect('view-atm-login-credentials-details')
        else:
            form.fields['s_n'].widget.attrs['readonly'] = True
            
    except:
        messages.warning(
            request, f'Something went wrong')
    return render(request, 'ATMStatus/atm_login_credentials_details/modify_atm_login_credentials_details.html', {'form': form})


# ->Delete atm login credentials details
def delete_atm_login_details(request, pid):
    delete_atm_login_details = ATMLoginCredentialsDetails.objects.get(id=pid)
    if request.method == 'POST':
        messages.success(
            request, f"ID '{delete_atm_login_details.id}' ATM login credentials details has been successfully deleted!")

        delete_atm_login_details.delete()
        return redirect('view-atm-login-credentials-details')

    return render(request, 'ATMStatus/atm_login_credentials_details/delete_atm_login_credentials_details.html', {'delete_atm_login_details': delete_atm_login_details})

# ->exporting to excel


def export_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Report.xls'
    work_book = xlwt.Workbook(encoding='utf-8')
    work_sheet_name = work_book.add_sheet('Data')
    row_nu = 0
    header_font_style = xlwt.XFStyle()
    header_font_style.font.bold = True
    columns = [
        'SN.',
        'Branch Name',
        'Branch Code',
        'ATM IP',
        'VNC Password',
        'RAdmin Username',
        'RAdmin Password',
        'ATM Journal Username',
        'ATM Journal Password'
    ]

    for column_num in range(len(columns)):
        work_sheet_name.write(row_nu, column_num,
                              columns[column_num], header_font_style)

    body_font_style = xlwt.easyxf(
        'font: bold 1, name Tahoma, height 160;'
        'align: vertical center, horizontal center, wrap on;'
        'borders: left thin, right thin, top thin, bottom thin;'
        'pattern: pattern solid '
    )

    body_rows = ATMLoginCredentialsDetails.objects.all().values_list(
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

    for row in body_rows:
        print
        row_nu += 1
        for col_num in range(len(row)):
            work_sheet_name.write(
                row_nu, col_num, row[col_num], body_font_style)

    work_book.save(response)
    return response

#=> view all branch details

# class BranchDetailsListView(ListView):
#     query_set = ''
#     # try:        
#     test=db_connection_string.connection_string()           
#     query_set = 'exec sp_view_branch_details'
#     select_cursor = test.execute(query_set)
#     # all_branch_details = BranchDetails.objects.all()
#     model= tbl_branch_details
#     template_name = 'ATMStatus/branch_details/view_branch_details.html'
#     context_object_name = 'select_cursor'
#     paginate_by = 8
#     # except:
#     #      print('error in connection string')
    
def view_branch_details(request):    
              
    con_string=db_connection_string.connection_string()          
    query_set = 'exec sp_view_branch_details'
    select_cursor = con_string.execute(query_set) 
   
    return render(request,'ATMStatus/branch_details/view_branch_details.html',{'branch_details':select_cursor})
   

'''
    Add new branch details
''' 
def add_branch_details(request):  

    result = ''
    try:  
        form = BranchDetailsForm()   
        # total_row = BranchDetails.objects.all().count()
        total_row = sql_operation_branch_details.get_total_number_of_row()   

        if request.method == 'POST':
            form = BranchDetailsForm(request.POST)

            if form.is_valid():
                post_branch_name = form.cleaned_data.get('branch_name')   
                post_s_n = form.cleaned_data.get('s_n')          
                # is_branch_name_exists = BranchDetails.objects.filter(branch_name=post_branch_name).values('id')
                is_branch_name_exists = sql_operation_branch_details.get_branch_name(post_branch_name)
                
                post_branch_code = form.cleaned_data.get('branch_code')
          
                # is_branch_code_exists = BranchDetails.objects.filter(branch_code=post_branch_code).values('id')
                is_branch_code_exists = sql_operation_branch_details.get_branch_code(post_branch_code)    
                    
                branch_code_pattern = re.compile("[0-9][0-9]")
                

                if is_branch_name_exists:
                    messages.warning(request,f"'{post_branch_name}' branch name is already exists.")
                elif is_branch_code_exists:
                    messages.warning(request,f"'{post_branch_code}' branch code is already exists.")
                elif int(post_branch_code) <= 0:
                    
                    messages.warning(request,f"'{post_branch_code}'is not a valid branch code.")
                elif  not branch_code_pattern.match(post_branch_code):
                    messages.warning(request,f" Please follow [000] branch code.")
                else:
                    result = sql_operation_branch_details.add_branch_details(post_s_n,post_branch_name,post_branch_code)
                   
                    try:
                        if result:    
                            result.commit()           
                            messages.success(request,f"'{post_branch_name}' branch name has been successfully added.")
                            return redirect('view-all-branch-details')
                    except:                        
                        messages.error(request,f" Unable to insert data")

                    finally:                        
                        result.close()
                        
        else:
            form.fields['s_n'].initial = total_row + 1
            form.fields['s_n'].widget.attrs['readonly'] = True
       
    except:     
        messages.warning(request,f"Something went wrong in input data. Please check input type.")  

    form.fields['s_n'].widget.attrs['readonly'] = True
    return render(request,'ATMStatus/branch_details/add_branch_details.html',{'form':form})


'''
 Modify/edit particular branch details
 '''
def modify_branch_details(request,pid):
    try:
        # branch_data_details = BranchDetails.objects.get(id=pid)  
        particular_branch_details = sql_operation_branch_details.get_particular_branch_details(pid)    
        form = BranchDetailsForm()
        if request.method == 'POST':
            # form = BranchDetailsForm(request.POST, instance= particular_branch_details)
            form =  BranchDetailsForm(request.POST)
            
            if form.is_valid():            
                s_n = form.cleaned_data.get('s_n')
                branch_name = form.cleaned_data.get('branch_name')
                branch_code = form.cleaned_data.get('branch_code')
                update_result = sql_operation_branch_details.update_branch_details(pid,s_n,branch_name,branch_code)         
                
                try:
                    if update_result:            
                        update_result.commit()
                        previous_sn = ''
                        previous_branch_name = ''
                        previous_branch_code = ''
                        for value  in particular_branch_details: 
                            previous_sn = value[0]
                            previous_branch_name = value[1]
                            previous_branch_code = value[2]

                        messages.success(request,f''' Branch ID '{pid}' has been successfully updated and details are\n
                        ({previous_sn} to "{s_n}"),
                        ({previous_branch_name} to "{branch_name}"),
                        ({previous_branch_code} to "{branch_code}")
                        .''')
                        return redirect('view-all-branch-details')
                except:                                      
                        messages.error(request,f" Unable to update data")

                finally:                        
                    update_result.close()
        else:
            for value  in particular_branch_details:            
                # form = BranchDetailsForm(initial={'s_n':row[0],'branch_name':row[1],'branch_code':row[2]})
                form.fields['s_n'].initial = value[0]
                form.fields['s_n'].widget.attrs['readonly'] = True
                form.fields['branch_name'].initial = value[1]
                form.fields['branch_code'].initial = value[2]
    
    except:     
        messages.error(request,f"Something went wrong") 

        
    return render(request,'ATMStatus/branch_details/modify_branch_details.html',{'form':form})


def delete_branch_details(request,pid):
    try:
        # delete_branch_detail = BranchDetails.objects.get(id=pid)        
        print('post')
        print(request.method)
        if request.method == 'POST':  
            print('delete_result')
            delete_result = sql_operation_branch_details.delete_branch_details(pid)  
           
            try:
                if delete_result:
                    delete_result.commit()                   
                    messages.success(request,f" Branch details (ID '{pid}') have been successfully deleted.")
                    return redirect('view-all-branch-details')
            except:
                messages.error(request,f" Unable to delete branch details ID '{pid}' ")

            finally:                        
                 delete_result.close()
                

    except:     
        messages.error(request,f"Something went wrong") 

    return render(request,'ATMStatus/branch_details/delete_branch_details.html',{'delete_branch_details':pid})     

# class AtmDetailsCreateView(CreateView):
#     form_class = AtmDetailsForm
#     success_url = '/ATMStatus/viewallatmdetails/'
#     template_name = 'ATMStatus/atmdetails_form.html/'

#     def get_initial(self):

#         total_row = AtmDetails.objects.all().count()
#         form.fields['s_n'].widget.attrs['readonly'] = True
#         # recipe = get_object_or_404(AtmDetails, slug=self.kwargs.get('slug'))

#         return {

#             's_n': total_row + 1
#         }

#     def form_valid(self, form):
#         total_row = AtmDetails.objects.all().count()
#         if form.is_valid():
#             valid_sn = form.cleaned_data.get('s_n')
#             if valid_sn < 0:
#                 messages.warning(
#                     self.request, f'Please provide valid serial number i.e sn should not be in negative number.')
#                 return super().form_invalid(form)
#             else:
#                 return super().form_valid(form)


#
#     # print('test1')
#     # sn = request.POST.get("inputSN")
#     # branch_name = request.POST.get("inputBranchName")
#     # problem =  request.POST.get('inputProblem')
#     # remarks = request.POST.get('inputRemarks')
#     # terminal_id = request.POST.get('inputTerminalId')
#     # atm_terminal_name =  request.POST.get('inputAtmTerminalName')
#     # atm_ip_address = request.POST.get('inputAtmIpAddress')
#     # switch_ip_address =  request.POST.get('inputSwitchIpAddress')
#     # port_number =  request.POST.get('inputAtmPortNumber')
#     #
#     # view_atm_status =  ViewATMStatus(
#     #                                 s_n = sn,
#     #                                  branch_name=branch_name,
#     #                                  problem=problem,
#     #                                  remarks=remarks,
#     #                                  terminal_id = terminal_id,
#     #                                  atm_terminal_name=atm_terminal_name,
#     #                                  atm_ip_address=atm_ip_address,
#     #                                  switch_ip_address=switch_ip_address,
#     #                                  port_number=port_number
#     #                                  )
#     # view_atm_status.save()
#     # print('test2')
#     # return render(request, 'AddATMStatusForm.html')

'''
Adding new terminal ID
'''


# @csrf_exempt
# def serialize(request):

#     if request.method == 'GET':
#         all_id = AtmTerminalIdDetails.objects.all()
#         serialize = AtmTerminalIdDetailsSerializer(all_id, many=True)
#         return JsonResponse(serialize.data, safe=False)
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serialize = AtmTerminalIdDetailsSerializer(data=data)
#         if serialize.is_valid():
#             serialize.save()
#             return JsonResponse(serialize.data, status=200)
#         return JsonResponse(serialize.errors, status=400)

@api_view(['GET', 'POST'])
def serialize(request):

    if request.method == 'GET':
        all_id = AtmTerminalIdDetails.objects.all()
        serialize = AtmTerminalIdDetailsSerializer(all_id, many=True)
        return Response(serialize.data)
    elif request.method == 'POST':

        serialize = AtmTerminalIdDetailsSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_201_CREATED)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
# def terminal_serialize(request, pk):
#     try:
#         all_id = AtmTerminalIdDetails.objects.get(id=pk)
#     except AtmTerminalIdDetails.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         seralizer = AtmTerminalIdDetailsSerializer(all_id)
#         return JsonResponse(seralizer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = AtmTerminalIdDetailsSerializer(all_id, data=data)
#         print('test1')
#         if serializer.is_valid():
#             print('test2')
#             serializer.save()
#             print('test3')
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         print('deleted1')
#         all_id.delete()
#         print('deleted2')
#         return HttpResponse(status=204)

@api_view(['GET', 'PUT', 'DELETE'])
def terminal_serialize(request, pk):
    try:
        all_id = AtmTerminalIdDetails.objects.get(id=pk)
    except AtmTerminalIdDetails.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        seralizer = AtmTerminalIdDetailsSerializer(all_id)
        return Response(seralizer.data)

    elif request.method == 'PUT':
        serializer = AtmTerminalIdDetailsSerializer(all_id, data=request.data)
        print('test1')
        if serializer.is_valid():
            print('test2')
            serializer.save()
            print('test3')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        print('deleted1')
        all_id.delete()
        print('deleted2')
        return HttpResponse(status=204)


class terminalAPIClass(APIView):

    def get(self, request):
        terminal_id = AtmTerminalIdDetails.objects.all()
        serialized = AtmTerminalIdDetailsSerializer(terminal_id, many=True)
        return Response(serialized.data)

    def post(self, request):
        serialized = AtmTerminalIdDetailsSerializer(
            data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
