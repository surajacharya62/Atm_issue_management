from django import forms
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponseRedirect
from .models import ViewATMStatus


class ContactForm(forms.Form):
    name = forms.CharField(max_length=10, label='Your Name')
    email = forms.EmailField(required=False,label='Your Email Address')
    subject = forms.CharField(max_length=50)
    messsage = forms.Textarea()





