from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework.parsers import JSONParser
from .models import(
    AtmDetails,
    AtmTerminalIdDetails,
    AtmIssueDetails,
    ATMLoginCredentialsDetails)
from ATMStatus.forms.AtmDetailsForm import AtmDetailsForm
from ATMStatus.forms.AddTerminalIdDetailsForm import AddTerminalIdForm
from ATMStatus.forms.atmissuedetails_form import AtmIssueDetailsForm
from ATMStatus.forms.atm_login_credentials_details_form import ATMLoginCredentialsDetailsForm
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


def index(request):
    atm_fields = AtmIssueDetails.objects.all()

    return render(request, 'View_ATM_Status.html', {'atm_fields': atm_fields})

# -> view all all terminal id details


def view_atm_terminal_id_details(request):
    all_atm_terminal_id = AtmTerminalIdDetails.objects.all()
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

    print(os.getenv('test'))
    print(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME)

    return render(request, 'ATMStatus/atm_terminal_details/view_atm_terminal_id_details.html', {'all_atm_terminal_id': all_atm_terminal_id})


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
            is_terminal_id_already_exist = AtmTerminalIdDetails.objects.filter(
                atm_terminal_id=atm_id).values('id')
            atm_id_pattern = re.compile('JBBL[0-9][0-9][0-9][0-9]')
            if is_terminal_id_already_exist:
                messages.warning(
                    request, f'Your provided terminal id is already exists.')
            elif not atm_id_pattern.match(atm_id):
                print('print1')
                # error_message = 'Please follow the [JBBL_branchid_01]'
                messages.warning(
                    request, f'Please follow the [JBBL_branchid_01]')
            else:
                messages.success(
                    request, 'New ATM terminal has been added successfully.')
                add_terminal_id.save()
                return redirect(view_atm_terminal_id_details)

    return render(request, 'ATMStatus/atm_terminal_details/add_terminal_id_details.html', {'add_terminal_id': add_terminal_id, 'atm_id_pattern_error': error_message})


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

    return render(request, 'ATMStatus/atm_terminal_details/modify_atm_terminal_id_details.html', {'modify_atm_terminal_id': modify_atm_terminal_id, 'atm_id_pattern_error': error_message})


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

    return render(request, 'ATMStatus/atm_terminal_details/delete_atm_terminal_id_details.html', {'delete_atm_id': deleted_atm_id})


# class ATMTerminalIdDetailsDeleteView(DeleteView):
#     model = AtmTerminalIdDetails
#     success_url = '/ATMStatus/viewallatmterminalid'


# -> Viewing atm details.
def view_atm_details(request):
    all_atm_details = AtmDetails.objects.all()
    return render(request, 'viewatmdetails.html', {'all_atm_details': all_atm_details})


class AtmDetailsListView(ListView):
    all_atm_details = AtmDetails.objects.all()
    model = AtmDetails
    template_name = 'view_atm_details.html'
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
    template_name = 'ATMStatus/atm_issue_details/view_atm_issue_details.html'
    context_object_name = 'all_atm_issue_details'
    paginate_by = 10


# -> Adding atm issue details
def add_atm_issue_details(request):
    form = AtmIssueDetailsForm()
    total_row = AtmIssueDetails.objects.all().count()
    # try:
    if request.method == 'POST':
        form = AtmIssueDetailsForm(request.POST)
        if form.is_valid():

            is_valid_branch_code = form.cleaned_data.get('branch_code')

            if is_valid_branch_code == 'Please select branch code':
                messages.error(request, f'Please provide valid branch code')
            else:
                form.save()
                messages.success(
                    request, f"ATM issue details has been successfully added!")

                return redirect('view-atm-issue-details')

    else:

        form.fields['s_n'].initial = total_row + 1
        form.fields['s_n'].widget.attrs['readonly'] = True

    # except:
    #     messages.warning(
    #         request, f'Something went wrong')

    return render(request, 'ATMStatus/atm_issue_details/add_atm_issue_details.html', {'form': form})

 # -> Adding atm issue details


def modify_atm_issue_details(request, pid):
    update_atm_issue = AtmIssueDetails.objects.get(id=pid)
    form = AtmIssueDetailsForm(instance=update_atm_issue)
    # try:
    if request.method == 'POST':
        form = AtmIssueDetailsForm(request.POST, instance=update_atm_issue)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"'{update_atm_issue.id}' ATM issue details has been successfully modified!")
            return redirect('view-atm-issue-details')

    # except:
    #     messages.warning(
    #         request, f'Something went wrong')

    return render(request, 'ATMStatus/atm_issue_details/modify_atm_issue_details.html', {'form': form})


# ->Deleting the issue details


def delete_atm_issue_details(request, pid):
    delete_atm_issue_details = AtmIssueDetails.objects.get(id=pid)
    if request.method == 'POST':
        messages.success(
            request, f"'{delete_atm_issue_details.id}' ATM issue details has been successfully deleted!")
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
    paginate_by = 5


def add_atm_login_credentials_details(request):
    form = ATMLoginCredentialsDetailsForm()
    total_row = ATMLoginCredentialsDetails.objects.all().count()
    try:
        if request.method == 'POST':
            form = ATMLoginCredentialsDetailsForm(request.POST)
            if form.is_valid():
                atm_details = form.cleaned_data.get('branch_name')
                is_atm_detail_already_exists = ATMLoginCredentialsDetails.objects.filter(
                    branch_name=atm_details).values('id')
                if is_atm_detail_already_exists:
                    messages.warning(
                        request, f'Your provided branch atm details is already exists.')
                else:
                    form.save()
                    messages.success(
                        request, f"ATM login credentials details has been successfully added!")
                    return redirect('view-atm-login-credentials-details')

        else:

            form.fields['s_n'].initial = total_row + 1
            form.fields['s_n'].widget.attrs['readonly'] = True

    except:
        messages.warning(
            request, f'Something went wrong')

    return render(request, 'ATMStatus/atm_login_credentials_details/add_atm_login_credentials_details.html', {'form': form})

# -> Modify and update the atm login credentials details


def modify_atm_login_credentials_details(request, pid):

    update_atm_credentials = ATMLoginCredentialsDetails.objects.get(id=pid)
    form = ATMLoginCredentialsDetailsForm(instance=update_atm_credentials)
    try:
        if request.method == 'POST':
            form = ATMLoginCredentialsDetailsForm(
                request.POST, instance=update_atm_credentials)
            if form.is_valid():
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
