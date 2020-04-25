from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import AtmDetails, AtmTerminalIdDetails, AtmIssueDetails
from .AtmDetailsForm import AtmDetailsForm
from .AddTerminalIdDetailsForm import AddTerminalIdForm
from django.urls import reverse
from django.contrib import messages
import re
from django.views.generic import (
    CreateView, DeleteView, ListView
)


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
    delete_terminal_id = AtmTerminalIdDetails.objects.get(id=pid)
    deleted_atm_id = delete_terminal_id.atm_terminal_id

    if request.method == "POST":
        print(delete_atm_terminal_id)
        print('delete2')
        messages.success(
            request, f"ATM ID '{deleted_atm_id}' has been successfully deleted!")
        delete_terminal_id.delete()
        return redirect(view_atm_terminal_id_details)

    return render(request, 'DeleteATMTerminalIdDetails.html', {'delete_atm_id': deleted_atm_id})


class ATMTerminalIdDetailsDeleteView(DeleteView):
    model = AtmTerminalIdDetails
    success_url = '/ATMStatus/viewallatmterminalid'


# -> Viewing atm details.


def view_atm_details(request):
    all_atm_details = AtmDetails.objects.all()
    return render(request, 'viewatmdetails.html', {'all_atm_details': all_atm_details})


class AtmDetailsListView(ListView):
    all_atm_details = AtmDetails.objects.all()

    model = AtmDetails
    template_name = 'viewatmdetails.html'
    context_object_name = 'all_atm_details'

    paginate_by = 10


def add_atm_details(request):
    form = AtmDetailsForm()
    total_row = AtmDetails.objects.all().count()
    try:
        if request.method == 'POST':
            form = AtmDetailsForm(request.POST)
            if form.is_valid():
                is_valid_atm_ip_address = form.cleaned_data.get(
                    'atm_ip_address')
                is_valid_switch_ip_address = form.cleaned_data.get(
                    'switch_ip_address')
                is_valid_branch_code = form.cleaned_data.get('branch_code')
                is_valid_branch_name = form.cleaned_data.get('branch_name')

                # test = AtmDetails.objects.values_list(
                #     'id').get(branch_name=valid_branch_name)

                is_branchname_already_exists = AtmDetails.objects.filter(
                    branch_name=is_valid_branch_name).values('id')

                pattern = re.compile('10[.][0-9][0-9][.][0-9][0-9]')
                if is_valid_branch_code <= 0:
                    messages.warning(
                        request, f'Your provided branch code is not valid.')
                elif is_branchname_already_exists:
                    messages.warning(
                        request, f'Your provided branch name is already exists.')
                elif not pattern.match(is_valid_atm_ip_address):
                    messages.warning(
                        request, f'Please follow the [10.00.00.00] pattern in ATM IP Address')
                elif not pattern.match(is_valid_switch_ip_address):
                    messages.warning(
                        request, f'Please follow the [10.00.00.00] pattern in Switch IP Address')
                else:
                    form.save()
                    return redirect('view-all-atm-details')

        else:

            form.fields['s_n'].initial = total_row + 1
            form.fields['s_n'].widget.attrs['readonly'] = True
            form.fields['switch_port_number'].widget.attrs['readonly'] = True
    except:
        messages.warning(
            request, f'Something went wrong')

    return render(request, 'ATMStatus/atmdetails_form.html', {'form': form})

# modifying the atm details


def modify_atm_details(request, pid):

    atm_details = AtmDetails.objects.get(id=pid)
    form = AtmDetailsForm(instance=atm_details)

    # try:
    if request.method == 'POST':
        form = AtmDetailsForm(request.POST, instance=atm_details)
        if form.is_valid():
            is_valid_atm_ip_address = form.cleaned_data.get('atm_ip_address')
            is_valid_switch_ip_address = form.cleaned_data.get(
                'switch_ip_address')
            is_valid_branch_name = form.cleaned_data.get('branch_name')

            pattern = re.compile('10[.][0-9][0-9][.][0-9][0-9]')

            if not pattern.match(is_valid_atm_ip_address):
                messages.warning(
                    request, f'Please follow the [10.00.00.00] pattern in ATM IP Address')
                form.fields['s_n'].widget.attrs['readonly'] = True
                form.fields['switch_port_number'].widget.attrs['readonly'] = True
            elif not pattern.match(is_valid_switch_ip_address):
                messages.warning(
                    request, f'Please follow the [10.00.00.00] pattern in Switch IP Address')
                form.fields['s_n'].widget.attrs['readonly'] = True
                form.fields['switch_port_number'].widget.attrs['readonly'] = True
            else:
                form.save()
                return redirect('view-all-atm-details')

    else:

        form.fields['s_n'].widget.attrs['readonly'] = True
        form.fields['switch_port_number'].widget.attrs['readonly'] = True
    # except:
    #     pass
        # messages.warning(
        #     request, f'Something went wrong')

    return render(request, 'ATMStatus/modifyatmdetails_form.html', {'form': form})


def delete_atm_details(request, pid):
    delete_atm_details = AtmDetails.objects.get(id=pid)
    if request.method == 'POST':
        delete_atm_details.delete()
        messages.success(
            request, f"'{delete_atm_details}' ATM details has been successfully deleted!")
        return redirect('view-all-atm-details')

    return render(request, 'ATMStatus/deleteatmdetails_form.html', {'delete_atm_details': delete_atm_details})


class AtmIssueDetailsListView(ListView):
    all_atm_issue_details = AtmIssueDetails.objects.all()
    model = AtmIssueDetails
    context = {
        'atmissuedetails': all_atm_issue_details

    }
    template_name = 'ATMStatus/view_atm_issue_details.html'
    context_object_name = 'all_atm_issue_details'
    paginate_by = 10

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
