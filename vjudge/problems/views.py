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
import re
import requests
import string
from accounts.models import Profile

# Create your views here.

def cmp(a, b):
     return [c for c in a if c.isalpha()] == [c for c in b if c.isalpha()]

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

        #tags[i.pid].append(ii)

    return render(request, 'front/allproblems.html',{'allproblem':allproblem})

def problem(request,pk):

    language = ['Java','NodeJS','C','C++','PHP','Python 2','Python 3','Kotlin','GO Lang','C#']


    details = Problem.objects.get(pk=pk)
    p = details.pexinput
    cleanr = re.compile(r'<[^>]+>')
    p = re.sub(cleanr,'',p)
    print(p)


    if request.method == 'POST':
        p = details.pexinput
        cleanr = re.compile(r'<[^>]+>')
        p = re.sub(cleanr,'',p)

        q = details.pexoutput
        cleanr = re.compile(r'<[^>]+>')
        q = re.sub(cleanr,'',q)
        lan = request.POST.get('language')
        code = request.POST.get('code')
        lang = 'cpp17'
        ver = 0
        if lan == 'Java':
            lang = 'java'
            ver = 3
        elif lan == 'C':
            lan = 'c'
            ver = 4
        elif lan == 'C++':
            lan = 'cpp17'
            ver = 0
        elif lan == 'PHP':
            lan = 'php'
            ver = 3
        elif lan == 'Python 2':
            lan = 'python2'
            ver = 2
        elif lan == 'Python 3':
            lan = 'python3'
            ver = 3
        elif lan == 'GO Lang':
            lan = 'go'
            ver = 3
        elif lan == 'C#':
            lan = 'csharp'
            ver = 3
        elif lan == 'Kotlin':
            lan = 'kotlin'
            ver = 2
        elif lan == 'NodeJS':
            lan = 'nodejs'
            ver = 3

        task = {"clientId": "c2eed3b46d56379f836878a45aadb27f", "clientSecret":"3c9b309578bd148a31033a22a62ae149deed3a00f3e5658937e2d34b6f165203", "script": code , "stdin" : p, "language" : lang, "versionIndex": ver}
        resp = requests.post("https://api.jdoodle.com/v1/execute", json = task)
        resp = resp.json()
        print(resp)
        op = resp['output']
        timelimit = resp['cpuTime']
        memorylimit = resp['memory']

        cleanr = re.compile(r'<[^>]+>')
        op = re.sub(cleanr,'',op)
        gtl = float(details.ptimelimit)
        stl = float(resp['cpuTime'])
        gml = float(details.pmemorylimit) * 1024
        sml = float(resp['memory'])

        usr = request.user.username
        info = Profile.objects.get(uname = usr)
        tot = int(info.totalsub +1)
        print(tot)
        info.totalsub = tot
        info.save()
        if stl <= gtl :
            if sml<=gml :
                if cmp(op,q) == True:
                    tot = info.totalac + 1
                    info.totalac = tot
                    info.save()
                else:
                    tot = info.totalwa + 1
                    info.totalwa = tot
                    info.save()
            else:
                tot = info.totalme + 1
                info.totalme = tot
                info.save()
        else:
            tot = info.totaltle + 1
            info.totaltle = tot
            info.save()
        print(cmp(q,op))
        print(q)
        print(op)

    return render(request, 'front/problem.html',{'details':details,'language':language})

def submit(request):


    return render(request, 'front/submit.html')
