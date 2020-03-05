from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import ViewATMStatus
from .ContactForm import ContactForm
from .AddATMStatusForm import AddATMStatusForm
from django.urls import reverse



def index(request):
    atm_fields = ViewATMStatus.objects.all()
    return render(request,'View_ATM_Status.html',{'atm_fields':atm_fields})

def view_atm_issue(request):
    atm_fields = ViewATMStatus.objects.all()
    return render(request,'View_ATM_Status.html',{'atm_fields':atm_fields})

def add_form_status(request, pid=0):

    if request.method == "GET":
        if pid == 0:
            addform = AddATMStatusForm()
            return render(request,'AddATMStatusForm.html',{'addform':addform})
        else:
            addform = ViewATMStatus.objects.get(id=pid)
            new = AddATMStatusForm(instance=addform)
            return render(request,'AddATMStatusForm.html',{'addform':new})

    else:
        add_form = AddATMStatusForm(request.POST)
        if add_form.is_valid():
            try:
                add_form.save()
                return redirect(view_atm_issue)
            except:
                pass



    # print('test1')
    # sn = request.POST.get("inputSN")
    # branch_name = request.POST.get("inputBranchName")
    # problem =  request.POST.get('inputProblem')
    # remarks = request.POST.get('inputRemarks')
    # terminal_id = request.POST.get('inputTerminalId')
    # atm_terminal_name =  request.POST.get('inputAtmTerminalName')
    # atm_ip_address = request.POST.get('inputAtmIpAddress')
    # switch_ip_address =  request.POST.get('inputSwitchIpAddress')
    # port_number =  request.POST.get('inputAtmPortNumber')
    #
    # view_atm_status =  ViewATMStatus(
    #                                 s_n = sn,
    #                                  branch_name=branch_name,
    #                                  problem=problem,
    #                                  remarks=remarks,
    #                                  terminal_id = terminal_id,
    #                                  atm_terminal_name=atm_terminal_name,
    #                                  atm_ip_address=atm_ip_address,
    #                                  switch_ip_address=switch_ip_address,
    #                                  port_number=port_number
    #                                  )
    # view_atm_status.save()
    # print('test2')
    # return render(request, 'AddATMStatusForm.html')


def modify_atm_issue(request, pid):
    addform = ViewATMStatus.objects.get(pk=pid)
    if request.method == 'GET':
        update_issue = AddATMStatusForm(instance=addform)
        print('test1')
        print(update_issue.is_valid())
        print(update_issue)
        return render(request, 'ModifyATMIssue.html', {'atm_issue_update': update_issue})
    else:
        updated_issue = AddATMStatusForm(request.POST, instance=addform)
        print(updated_issue.is_valid())
        print(updated_issue)
        if updated_issue.is_valid():
            update = updated_issue.cleaned_data
            print(update)
            print('test2')
            try:
                print('test3')
                updated_issue.save()

                return redirect(view_atm_issue)
            except:
                pass
        #return render(request,'ModifyATMIssue.html',{'atm_issue_update':atm_issue_update})


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