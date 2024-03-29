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
import operator
from contests.models import Ranklist,Submission,Contest
import json
# Create your views here.

headers = {'content-type': 'application/json'}

def cmp(a, b):
     return [c for c in a if c.isalpha()] == [c for c in b if c.isalpha()]

def dashboard(request):

    return render(request, 'back/dashboard.html')

@login_required(login_url = '/loginPage/')
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
        psinput = request.POST.get('psinput')
        psoutput = request.POST.get('psoutput')
        ptags = request.POST.get('ptags')
        ptype = request.POST.get('ptype')
        pnote = request.POST.get('pnote')
        pshow = request.POST.get('pshow')
        b = Problem(ptitle=ptitle,ptimelimit=ptimelimit,pmemorylimit=pmemorylimit,pdescription=pdescription,pinput=pinput,poutput=poutput,pexinput=pexinput,pexoutput=pexoutput,ptags=ptags,ptype=ptype,pnote=pnote,pshow=pshow,psinput=psinput,psoutput=psoutput)
        b.save()
        return redirect('allproblems')
    return render(request, 'back/addproblem.html',{'type':type,'share':share})

def allproblems(request):
    allproblem = Problem.objects.all()

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
    cleanr = re.compile(r'<[^>]+>')

    input = details.psinput
    input = re.sub(cleanr,'',input)
    output = details.psoutput
    output = re.sub(cleanr,'',output)
    input = input.split(";")
    output = output.split(";")
    p = details.pexinput
    cleanr = re.compile(r'<[^>]+>')
    p = re.sub(cleanr,'',p)



    if request.method == 'POST':
        #Submissionid
        usr = request.user.username
        bb = Submission(user = usr)
        bb.save()
        subid = bb.submissionid

        lan = request.POST.get('language')
        code = request.POST.get('code')
        #lang = 'cpp17'
        ver = 0
        if lan == 'Java':
            lan = 'java'
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

        #submission language
        bb.language = lan
        bb.code = code
        bb.problemid = pk
        bb.save()

        details = Problem.objects.get(pk=pk)

        bb.problemtitle = details.ptitle
        bb.save()
        p = details.pexinput
        cleanr = re.compile(r'<[^>]+>')
        p = re.sub(cleanr,'',p)
        #output
        q = details.pexoutput
        cleanr = re.compile(r'<[^>]+>')
        q = re.sub(cleanr,'',q)


        p = p.split(";")
        q = q.split(";")

        ac = True

        pro = Profile.objects.get(uname = usr)

        for i in range(0,len(p)):
            inp = p[i]
            out = q[i]
            cleanr = re.compile(r'<[^>]+>')
            inp = re.sub(cleanr,'',inp)
            out = re.sub(cleanr,'',out)
            print(inp)
            print(out)
            print(code)

            task = {"clientId": "827646b49b0d2e078eb637d28a3d4202", "clientSecret":"f81ec97b9f03ef577968c605fd1b53fe67a6b3e74bc64f3eb3435e45cb5f0779", "script": code , "stdin" : inp, "language" : lan, "versionIndex": ver}
            resp = requests.post("https://api.jdoodle.com/v1/execute", headers=headers, json = json.dumps(task))
            resp = resp.json()
            #input
            print(resp)

            if resp['statusCode'] == 200:
                print(200)
                op = resp['output']
                timelimit = resp['cpuTime']
                memorylimit = resp['memory']

                cleanr = re.compile(r'<[^>]+>')
                op = re.sub(cleanr,'',op)

                gtl = float(details.ptimelimit)
                stl = (resp['cpuTime'])
                gml = float(details.pmemorylimit) * 1024
                sml = (resp['memory'])




                if str(stl) == 'None' or str(sml) == 'None':
                    bb.status = 'Syntex Error'
                    bb.save()
                    sub = pro.totalsub
                    sub += 1
                    pro.totalsub = sub
                    wa = pro.totalwa
                    wa += 1
                    pro.totalwa = wa
                    pro.save()
                    messages.info(request, "Syntex Error")
                    return redirect('problem', pk = pk)
                    ac = False
                    break

                else:
                    if float(stl) <= gtl :
                        print(1)
                        if float(sml)<=gml :
                            print(2)
                            if cmp(op,out) == True:
                                print(3)
                                continue
                            else:
                                bb.status = 'Worng Answer'
                                bb.save()
                                sub = pro.totalsub
                                sub += 1
                                pro.totalsub = sub
                                wa = pro.totalwa
                                wa += 1
                                pro.totalwa = wa
                                pro.save()
                                ac = False
                                messages.error(request, 'Wrong Answer')
                                break
                        else:
                            bb.status = 'Memory Limit'
                            bb.save()

                            sub = pro.totalsub
                            sub += 1
                            pro.totalsub = sub
                            me = pro.totalme
                            me += 1
                            pro.totalme = me
                            pro.save()
                            ac = False
                            messages.error(request, 'Memory Limit')
                            break
                    else:
                        bb.status = 'Time Limit'
                        bb.save()

                        sub = pro.totalsub
                        sub += 1
                        pro.totalsub = sub
                        tl = pro.totaltle
                        tl += 1
                        pro.totaltle = tl
                        pro.save()
                        ac = False
                        messages.error(request, 'Time Limit')
                        break

            else:
                bb.status = 'Worng Answer'
                bb.save()
                sub = pro.totalsub
                sub += 1
                pro.totalsub = sub
                wa = pro.totalwa
                wa += 1
                pro.totalwa = wa
                pro.save()
                ac = False
                messages.erroe(request, 'Wrong Answer')
                break

        if ac == True:
            print("ac")
            bb.status = 'Accepted'
            bb.save()

            sub = pro.totalsub
            sub += 1
            pro.totalsub = sub
            ac = pro.totalac
            ac += 1
            pro.totalac = ac
            pro.save()
            messages.success(request, 'Accepted')
        return redirect('profile')



    return render(request, 'front/problem.html',{'details':details,'language':language,'input':input,'output':output})
