from django.shortcuts import render , get_object_or_404, redirect
from .models import *
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.contrib.auth.decorators import login_required
import datetime
from django.utils.timezone import utc

# Create your views here.

def dashboard(request):

    return render(request, 'back/dashboard.html')

def addproblem(request):

    type = ['Easy','Hard','Mediam']
    share = ['Yes','No']
    if request.method == 'POST':
        ptitle = request.POST.get('ptitle')
        ptimelimit = request.POST.get('ptimelimit')
        pmemorylimit = request.POST.get('pmemorylimit')
        pdescription = request.POST.get('pdescription')
        pinput = request.POST.get('pinput')
        poutput = request.POST.get('poutput')
        pexinput = request.POST.get('pexinput')
        pexoutput = request.POST.get('pexoutput')
        ptags = request.POST.get('ptags')
        ptype = request.POST.get('ptype')
        pnote = request.POST.get('pnote')
        pid = request.POST.get('pid')
        pshow = request.POST.get('pshow')
        b = Problem(pid = pid, ptitle=ptitle,ptimelimit=ptimelimit,pmemorylimit=pmemorylimit,pdescription=pdescription,pinput=pinput,poutput=poutput,pexinput=pexinput,pexoutput=pexoutput,ptags=ptags,ptype=ptype,pnote=pnote,pshow=pshow)
        print(b)
        b.save()
    return render(request, 'back/addproblem.html',{'type':type,'share':share})

def allproblems(request):
    allproblem = Problem.objects.all()
    print(allproblem)

    return render(request, 'back/allproblems.html',{'allproblem':allproblem})

#for Geleral User
def viewproblems(request):
    allproblem = Problem.objects.all()
    print(allproblem)
    tags = {}
    for i in allproblem:
        ii = i.ptags
        ii = ii.split(",")
        tags[i.pid] = ii
        #tags[i.pid].append(ii)

    return render(request, 'front/allproblems.html',{'allproblem':allproblem, 'tags':tags})

def problem(request,pk):

    details = Problem.objects.get(pk=pk)

    return render(request, 'front/problem.html',{'details':details})

def submit(request):


    return render(request, 'front/submit.html')
