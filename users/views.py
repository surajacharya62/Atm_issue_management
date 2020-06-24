from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .UserForm import UserUpdateForm, ProfileUpdateForm, UserRegistrationForm
from users.login_form import LoginForm


@login_required
def register(request):
    form = ''
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(
                request, f"User '{username}' has been successfully created!")
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            messages.success(
                request, f"Your account has been successfully updated!")
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'profile.html', context)

def user_login(request):

    form = LoginForm()   
    # request.session['username'] = 'not logged in'
    # print(request.session['username'])
    print(request.user)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.user
        request.session['username'] = request.user
        if form.is_valid():
            request.session.set_expiry(60)
            return render(request,'logged_in.html',{'formuser':username})

    return render(request,'UserLogin.html',{'form':form})

def connection(request):
    form = LoginForm()
    if request.session.has_key('username'):
        username = request.session['username']
        return render(request,'logged_in.html',{'formuser':username}) 
        
    return render(request,'UserLogin.html',{'form':form})