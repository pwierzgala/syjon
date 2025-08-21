# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import password_change
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _

from apps.trainman.backends import fake_authenticate
from apps.trainman.forms import EmailForm, LoginForm, UsernameForm

TEMPLATE_ROOT = 'trainman/'


def user_profile(request):
    if request.method == "POST":
        username_form = UsernameForm(request.POST)
        email_form = EmailForm(request.POST)
        if request.POST.get('submit') == 'username':
            if username_form.is_valid():
                request.user.username = username_form.cleaned_data['username']
                try:
                    request.user.save()
                except IntegrityError:
                    messages.error(request, _(u'Username %s already exists. Try other name.' % request.user.username))
                else:
                    messages.success(request, _(u'Username has been changed'))
        elif request.POST.get('submit') == 'email':
            if email_form.is_valid():
                request.user.email = email_form.cleaned_data['email']
                request.user.save()
                messages.success(request, _(u'E-mail address has been changed'))
        else:
            messages.error(request, _(u'An error occured while saving user profile'))
    else:
        username_form = UsernameForm(initial={'username': request.user.username})
        email_form = EmailForm(initial={'email': request.user.email})
    
    kwargs = {'username_form': username_form, 'email_form': email_form}
    return render(request, TEMPLATE_ROOT + 'profile.html', kwargs)


# --------------------------------------------------------------
# --- LOGOUT
# --------------------------------------------------------------

def user_logout(request):
    
    login_user = None
    if 'admin_username' in request.session:
        try:
            username = request.session['admin_username']
            del request.session['admin_username']
            
            user = User.objects.get(username=username)
            login_user = fake_authenticate(user.username)
        except User.DoesNotExist:
            pass
        
    logout(request)
    if login_user:
        login(request, login_user)
    
    return redirect('syjon:home')


# --------------------------------------------------------------
# --- LOGIN
# --------------------------------------------------------------

def user_login(request):
    form = LoginForm()
    
    if request.method == "GET":
        next = request.GET.get('next', '')
        return render(request, TEMPLATE_ROOT + 'login.html', {'form': form, 'next': next})
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if 'next' in request.POST and request.POST['next'] != '':
                    return redirect(request.POST['next'])
                else:
                    return redirect('syjon:home')
            else:
                messages.error(request, _(u'Your profile is inactive.'))
                return redirect('trainman:login')
        else:
            messages.error(request, _(u'Username or password are incorrect.'))
            return redirect('trainman:login')

    return render(request, TEMPLATE_ROOT + 'login.html', {'form': form})


# --------------------------------------------------------------
# --- PASSWORD CHANGE
# --------------------------------------------------------------

def user_password_change(request):
    return password_change(
        request,
        template_name=TEMPLATE_ROOT + 'password_change.html',
        post_change_redirect=reverse('trainman:password-change-done')
    )


def user_password_change_done(request):
    messages.success(request, _(u'Password has been changed.'))
    return password_change(
        request,
        template_name=TEMPLATE_ROOT + 'password_change.html',
        post_change_redirect=reverse('trainman:password-change-done')
    )
