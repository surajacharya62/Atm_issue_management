from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import AtmDetails, AtmTerminalIdDetails, AtmIssueDetails
from .AtmDetailsForm import AtmDetailsForm
from .AddTerminalIdDetailsForm import AddTerminalIdForm
from django.urls import reverse
from django.contrib import messages
import re


def index(request):
    atm_fields = AtmIssueDetails.objects.all()
    return render(request, 'View_ATM_Status.html', {'atm_fields': atm_fields})


def add_terminal_id_details(request):
    add_terminal_id = ''
    error_message = ''
    if request.method == "GET":
        add_terminal_id = AddTerminalIdForm()
        total_row = AtmTerminalIdDetails.objects.all().count()
        total_row += 1
        add_terminal_id.fields['s_n'].initial = total_row
        add_terminal_id.fields['s_n'].widget.attrs['readonly'] = True
    else:
        add_terminal_id = AddTerminalIdForm(request.POST)
        if add_terminal_id.is_valid():
            atm_id = add_terminal_id.cleaned_data.get('atm_terminal_id')
            atm_id_pattern = re.compile('JBBL[0-9][0-9][0-9][0-9]')
            if not atm_id_pattern.match(atm_id):
                print('print1')
                # error_message = 'Please follow the [JBBL_branchid_01]'
                messages.warning(
                    request, f'Please follow the [JBBL_branchid_01]')
            else:
                print('print2')
                add_terminal_id.save()
                return redirect(view_atm_terminal_id_details)

    return render(request, 'AddTerminalIdDetails.html', {'add_terminal_id': add_terminal_id, 'atm_id_pattern_error': error_message})


def modify_atm_terminal_id(request, pid):
    update_terminal_id = AtmTerminalIdDetails.objects.get(id=pid)
    previous_atm_id = update_terminal_id.atm_terminal_id
    error_message = ''
    modify_atm_terminal_id = ''
    if request.method == "GET":
        modify_atm_terminal_id = AddTerminalIdForm(instance=update_terminal_id)
        total_row = AtmTerminalIdDetails.objects.all().count()
        total_row += 1
        modify_atm_terminal_id.fields['s_n'].initial = total_row
        modify_atm_terminal_id.fields['s_n'].widget.attrs['readonly'] = True
    else:
        modify_atm_terminal_id = AddTerminalIdForm(
            request.POST, instance=update_terminal_id)
        if modify_atm_terminal_id.is_valid():
            new_atm_id = modify_atm_terminal_id.cleaned_data.get(
                'atm_terminal_id')
            atm_id_pattern = re.compile('JBBL[0-9][0-9][0-9][0-9]')
            if not atm_id_pattern.match(new_atm_id):

                # error_message = 'Please follow the [JBBL_branchid_01]'
                messages.warning(
                    request, f'Please follow the [JBBL_branchid_01]')
            else:
                messages.success(
                    request, f"ATM ID '{previous_atm_id }' has been successfully modified to '{new_atm_id}'")
                modify_atm_terminal_id.save()
                return redirect(view_atm_terminal_id_details)

    return render(request, 'ModifyATMTerminalIdDetails.html', {'modify_atm_terminal_id': modify_atm_terminal_id, 'atm_id_pattern_error': error_message})


def delete_atm_terminal_id(request, pid):
    delete_terminal_id = AtmTerminalIdDetails.objects.all(id=pid)
    deleted_atm_id = delete_terminal_id.atm_terminal_id
    delete_atm_terminal_id = ''

    if request.method == "GET":
        delete_atm_terminal_id = AddTerminalIdForm(instance=delete_terminal_id)
        print(delete_atm_terminal_id)

    else:
        delete_atm_terminal_id = AddTerminalIdForm(
            request.POST, instance=delete_terminal_id)
        print('delete1')
        print(delete_atm_terminal_id)
        if delete_atm_terminal_id.is_valid():
            print('delete2')
            messages.success(
                request, f"ATM ID '{deleted_atm_id}' has been successfully deleted!")
            delete_atm_terminal_id.delete()
            return redirect(view_atm_terminal_id_details)

    return render(request, 'DeleteATMTerminalIdDetails.html', {'delete_atm_terminal_id': delete_atm_terminal_id, 'delete_atm_id': deleted_atm_id})


# -> Viewing atm details.


def view_atm_details(request):
    all_atm_details = AtmDetails.objects.all()
    return render(request, 'ViewAtmDetails.html', {'all_atm_details': all_atm_details})

# -> View atm issues details.


def view_atm_issue_details(request):
    all_atm_issue_details = AtmIssueDetails.objects.all(AtmDetails_id)
    # all_atm_details = AtmDetails.objects.all()
    # all_merge = all_atm_issue_details | all_atm_details
    # print(all_merge)
    return render(request, 'ViewAtmIssueDetails.html', {'all_atm_issue_details': all_atm_issue_details})
# def add_form_status(request, pid=0):
#     atm_details = ''
#     if request.method == "GET":
#         add_form = AddATMStatusForm()
#         count_row = AtmDetails.objects.all().count()
#         count_row += 1
#         atm_details.fields['s_n'].initial = count_row
#         atm_details.fields['s_n'].widget.attrs['readonly'] = True
#
#         print(count_row)
#         return render(request, 'AddATMStatusForm.html', {'addform': add_form})
#
#
#     else:
#
#         add_form = AddATMStatusForm(request.POST)
#
#         sn = add_form.fields['s_n']
#         print(sn)
#         if add_form.is_valid():
#             try:
#
#                 add_form.save()
#                 return redirect(index)
#             except:
#                 pass
#
#
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


def view_atm_terminal_id_details(request):
    all_atm_terminal_id = AtmTerminalIdDetails.objects.all()
    return render(request, 'ViewATMTerminalIdDetails.html', {'all_atm_terminal_id': all_atm_terminal_id})


# ->   Modifying and updating the issues.
def modify_atm_issue(request, pid):
    addform = AtmIssueDetails.objects.get(pk=pid)
    addform1 = AddATMStatusForm(instance=addform)
    addform1.fields['terminal_id'].widget.attrs['readonly'] = True
    atm_error_message = ''
    switch_error_message = ''
    if request.method == 'GET':
        addform = AddATMStatusForm(instance=addform)
        addform.fields['terminal_id'].widget.attrs['readonly'] = True
        # error = ''
        # return render(request, 'ModifyATMIssue.html', {'atm_issue_update': update_issue},{'error_message':error})
    else:
        addform = AddATMStatusForm(request.POST, instance=addform)

        if addform.is_valid():

            validate_switch_ip = addform.cleaned_data.get('switch_ip_address')

            validate_atm_ip = addform.cleaned_data.get('atm_ip_address')
            print(validate_atm_ip)
            pattern = re.compile('[0-9][0-9][.][0-9][.]')

            if not pattern.match(validate_atm_ip):
                atm_error_message = 'Please follow: (10.0.)'

            elif not pattern.match(validate_switch_ip):

                switch_error_message = 'Please follow: (10.0.)'

            else:
                addform.save()
                return redirect(view_atm_issue)

    return render(request, 'ModifyATMIssue.html', {'atm_issue_update': addform, 'atm_error_message': atm_error_message, 'switch_error_message': switch_error_message})


def update_atm_issue(request, pid):
    new_value = ViewATMStatus.objects.get(id=pid)
    print(new_value)
    print('update')
    update_issue = AddATMStatusForm(request.POST, instance=new_value)
    print(update_issue)
    if request.method == 'POST':
        if update_issue.is_valid():
            update = update_issue.cleaned_data
            try:
                update.save()
                return redirect(view_atm_issue)
            except:
                pass
    return render(request, 'ModifyATMIssue.html', {'new_value': new_value})


def delete_atm_issue(request, pid):
    delete_issue = ViewATMStatus.objects.get(id=pid)
    delete_issue.delete()
    return render(request, 'Viewe_ATM_Status.html')


def contact(request1):
    submitted = False
    if request1.method == 'POST':
        my_form = ContactForm(request1.POST)
        if my_form.is_valid():
            cd = my_form.cleaned_data
            submitted = True
            print(cd[0])
            # return HttpResponseRedirect('contact/?submitted=True')
            print('test1')
            return render(request1, 'contact.html', {'submittted': submitted})

    else:
        my_form = ContactForm()
        return render(request1, 'contact.html', {'my_form': my_form, 'submittted': submitted})

#
