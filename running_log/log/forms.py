# forms
from django.contrib.auth.models import User
from .models import Activity, AuthUser
from django.template import RequestContext
from django.shortcuts import render,render_to_response
from django.contrib.auth.models import User
from django.http import HttpResponse
from django import forms
import datetime


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ('activity_type','distance','time','shoe','conditions','location','comments')
    def save(self, commit=True):
        Activity = super(ActivityForm, self).save(commit = False)
        Activity.date = datetime.datetime.utcnow()
        if commit:
            Activity.save()
        return Activity

class UserForm(forms.ModelForm):
    password1 = forms.CharField(label="password",widget=forms.PasswordInput())
    password2 = forms.CharField(label="re-enter password",widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            msg = "Passwords don't match"
            raise forms.ValidationError("Password mismatch")
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit = False)
        user.is_staff = False
        user.is_active = True
        user.is_superuser = False
        user.set_password(self.clean_password2())
        user.date_joined = datetime.datetime.utcnow()
        if commit:
            user.save()
        return user
