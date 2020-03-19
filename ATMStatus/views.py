from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import AtmDetails,AtmTerminalIdDetails,AtmIssueDetails
from .AtmDetailsForm import AtmDetailsForm
from .AddTerminalIdDetailsForm import AddTerminalIdForm
from django.urls import reverse
from django.contrib import messages
import re



def index(request):
    atm_fields = AtmIssueDetails.objects.all()
    return render(request,'View_ATM_Status.html',{'atm_fields':atm_fields})


def add_terminal_id_details(request):
    add_terminal_id = ''
    if request.method == "GET":
        add_terminal_id = AddTerminalIdForm()
    else:
        add_terminal_id = AddTerminalIdForm(request.POST)
        if add_terminal_id.is_valid():
            add_terminal_id.save()
            return redirect(view_atm_terminal_id_details)

    return render(request, 'AddTerminalIdDetails.html', {'add_terminal_id': add_terminal_id})


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
    return render(request,'ViewATMTerminalIdDetails.html',{'all_atm_terminal_id':all_atm_terminal_id})

'''
    Modifying and updating the issues.
'''
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

    return render(request,'ModifyATMIssue.html',{'atm_issue_update':addform,'atm_error_message':atm_error_message, 'switch_error_message':switch_error_message})


def update_atm_issue(request,pid):
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
    return render(request,'ModifyATMIssue.html',{'new_value':new_value})


def delete_atm_issue(request,pid):
    delete_issue = ViewATMStatus.objects.get(id=pid)
    delete_issue.delete()
    return render(request,'Viewe_ATM_Status.html')


def contact(request1):
    submitted = False
    if request1.method == 'POST':
        my_form = ContactForm(request1.POST)
        if my_form.is_valid():
            cd = my_form.cleaned_data
            submitted = True
            print(cd[0])
            #return HttpResponseRedirect('contact/?submitted=True')
            print('test1')
            return render(request1,'contact.html', {'submittted':submitted})

    else:
        my_form = ContactForm()
        return render(request1,'contact.html',{'my_form':my_form,'submittted':submitted})

#def user_registration(request):
    # if request.method == 'POST':
    #      form = RegistrationForm(request.POST)
    #      print('valid1')
    #      print(form)
    #      print(form.is_valid())
    #      if form.is_valid():
    #          print('valid2')
    #          form.save()
    #          return render(request, 'index.html')
    #      return render(request, 'index.html')
    # else:
    #     form = RegistrationForm()
    #     args= {'form':form}
    #     return render(request,'reg_form.html',args)