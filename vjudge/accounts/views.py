from django.shortcuts import render , get_object_or_404, redirect
from .models import *
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from problems.models import Problem
# Create your views here.
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm , ProfileUpdate
import datetime
from django.utils.timezone import utc
from contests.models import *
import requests


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                print(user)
                b = Profile(uname = user)
                b.save()
                return redirect('login')

        context = {'form': form}
        return render(request , 'front/register.html', context)

def updateprofilepicture(request):

    profile = get_object_or_404(Profile, uname=request.user.username)

    if request.method == 'POST':
        form = ProfileUpdate(request.POST or None, request.FILES or None, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = ProfileUpdate(instance=profile)
    return render(request, 'front/updateprofilepicture.html', {'form':form})

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect')
        context = {}
        return render(request , 'front/login.html', context)

@login_required(login_url = '/loginPage/')
def logoutUser(request):
    logout(request)
    return redirect('login')

def home(request):

    return render(request , 'front/home.html')

@login_required(login_url = '/loginPage/')
def profile(request):

    usr = request.user.username
    pro = Profile.objects.get(uname = usr )
    sub = Submission.objects.filter(user = request.user.username).order_by('-pk')
    ac = wa = th = 0
    for i in sub:
        if i.status == 'Accepted':
            ac += 1
        elif i.status == "Wrong Answer":
            wa += 1
        else:
            th += 1
    context = {
        'pro':pro,
        'sub':sub,
        'ac':ac,
        'wa':wa,
        'th':th
    }

    return render(request, 'front/profile.html', context)

@login_required(login_url = '/loginPage/')
def mysubmission(request):

    sub = Submission.objects.filter(user = request.user.username).order_by('-pk')
    problems = []
    for i in sub:
        x = get_object_or_404(Problem, pk=i.problemid)
        problems.append(x.ptitle)
    sub = zip(sub, problems)
    return render(request, 'front/mysubmission.html',{'sub':sub})
