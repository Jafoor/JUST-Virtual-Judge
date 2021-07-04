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
from problems.models import Problem
import re
import requests
import operator
from accounts.models import Profile
import json
#from contests.models import *

# Create your views here.

headers = {'content-type': 'application/json'}

def listToString(s):

    str1 = ""
    l = len(s)
    i = 0
    for ele in s:
        if(i != l-1):
            str1 += ele
            str1 += ','
        else:
            str1 += ele

    return str1


def setproblem(request,pk):

    probs = Problem.objects.all()
    if request.method == 'POST':
        val = request.POST.getlist('cars')
        if len(val)==0 or len(val)>10:
            messages.info(request, "You Must add 1 to 10 Problem")
            return redirect('setproblem',pk=pk)

        p = listToString(val)
        print(p)
        cnt = Contest.objects.get(pk=pk)
        cnt.problems = p
        cnt.save()
        return redirect('contest')


    return render(request, 'front/setproblem.html',{'probs': probs})

def contestpage(request):

    contests = Contest.objects.all()
    ended = []
    running = []
    upcomming = []
    for i in contests:


        sdate = i.cbeginingdate
        sdate = sdate.split("-")
        day = sdate[2]
        year = sdate[0]
        month = sdate[1]

        if len(str(day)) == 1:
            day = '0' + str(day)
        if len(str(month)) == 1:
            month = '0' + str(month)

        stime = i.cbeginingtime
        stime = stime.split(":")

        if len(str(stime[0])) == 1:
            stime[0] = '0' + str(stime[0])
        if len(str(stime[1])) == 1:
            stime[1] = '0' + str(stime[1])
        p1 = day+"/"+month+"/"+year+" "+stime[0]+":"+stime[1]+":"+str(00)
        startdate = datetime.datetime.strptime(p1, '%d/%m/%Y %H:%M:%S')
        today = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        today = datetime.datetime.strptime(today,'%d/%m/%Y %H:%M:%S')
        #print(today)
        #print(startdate)
        diff = today - startdate
        if int(diff.days) < 0:
            upcomming.append(i)
        ln = i.clength
        ln = ln.split(":")
        enddate = startdate + datetime.timedelta(hours=int(ln[0]), minutes = int(ln[1]), seconds=int(ln[2]) )

        finished = str(enddate.day)+"/"+str(enddate.month)+"/"+str(enddate.year)+" "+str(enddate.hour)+":"+str(enddate.minute)+":"+str(enddate.second)
        finished = datetime.datetime.strptime(finished, '%d/%m/%Y %H:%M:%S')
        #print(finished)
        diff1 = finished-today
        #print(diff)
        #print(diff1)
        if diff.days>=0 and diff1.days>=0:
            running.append(i)
        if diff.days>=0 and diff1.days<0:
            ended.append(i)
    return render(request, 'front/contestlist.html', {'contests' : contests, 'ended':ended, 'upcomming':upcomming, 'running':running})






def createcontestpage(request):

    if request.method == 'POST':

        title = request.POST.get('ctitle')
        description = request.POST.get('cdescription')
        beginingdate = request.POST.get('cbeginingdate')
        beginingtime = request.POST.get('cbeginingtime')
        length = request.POST.get('clength')
        ln = length.split(":")
        if len(ln) != 3:
            messages.info(request, "Correct Your Formate like hour:min:sec")
            return redirect('createcontest')

        if int(ln[0])>99 or int(ln[1])>59 or (int(ln[2])>59):
            messages.info(request, "Hour Should be lessthan 100, min and sec Should be lessthan 60")
            return redirect('createcontest')
        if int(ln[0])<0 or int(ln[1])<0 or (int(ln[2])<0):
            messages.info(request, "Time Can't be negative")
            return redirect('createcontest')

        password = request.POST.get('cpassword')
        b = Contest(ctitle = title , cbeginingdate = beginingdate, cdescription = description, cbeginingtime = beginingtime, clength = length, cpassword = password)
        b.save()
        #print(1111)
        #print(b.pk)
        return redirect('setproblem',pk=b.pk)

    return render(request, 'back/createcontest.html')





def contesttask(request,pk):

    contestdetails = Contest.objects.get(pk=pk)
    sdate = contestdetails.cbeginingdate
    sdate = sdate.split("-")
    day = sdate[2]
    year = sdate[0]
    month = sdate[1]

    if len(str(day)) == 1:
        day = '0' + str(day)
    if len(str(month)) == 1:
        month = '0' + str(month)

    stime = contestdetails.cbeginingtime
    stime = stime.split(":")

    if len(str(stime[0])) == 1:
        stime[0] = '0' + str(stime[0])
    if len(str(stime[1])) == 1:
        stime[1] = '0' + str(stime[1])
    if request.method == 'POST':
        try:
            gpassword = request.POST.get('gpassword')
        except:
            gpassword = ""
        cpassword = contestdetails.cpassword
        if cpassword == "":
            gpassword = cpassword
        if gpassword != cpassword:
            messages.info(request, "Incorrect Password")
            return redirect('contesttask',pk=contestdetails.pk)
        elif gpassword == cpassword:
               now = datetime.datetime.now()
               tyear = now.year
               tmonth = now.month
               tday = now.day
               if len(str(tday)) == 1:
                   tday = '0' + str(tday)
               if len(str(tmonth)) == 1:
                   tmonth = '0' + str(tmonth)
               thour = now.hour
               tmin = now.minute
               if len(str(thour)) == 1:
                   tday = '0' + str(tday)
               if len(str(tmonth)) == 1:
                   tmonth = '0' + str(tmonth)

               if (int(tyear) > int(year)) or (int(tmonth) > int(month) and int(tyear) == int(year)) or (int(tday) >= int(day) and int(tmonth) == int(month) and int(tyear) == int(year)) or (str(thour) > stime[0] and int(tday) >= int(day) and int(tmonth) == int(month) and int(tyear) == int(year)) or ((str(thour) == stime[0] and str(tmin) >= stime[1]) and int(tday) >= int(day) and int(tmonth) == int(month) and int(tyear) == int(year)):
                    return redirect('tasks', pk=contestdetails.pk)
               else:
                   messages.info(request, "Contest Not started Yet")
                   return redirect('contesttask', pk=contestdetails.pk)

    p = month+", "+day+", "+year+" "+stime[0]+":"+stime[1]+":"+str(00)
    p1 = day+"/"+month+"/"+year+" "+stime[0]+":"+stime[1]+":"+str(00)
    #for Length of the contest
    ln = contestdetails.clength
    ln = ln.split(":")
    startdate = datetime.datetime.strptime(p1, '%d/%m/%Y %H:%M:%S')
    enddate = startdate + datetime.timedelta(hours=int(ln[0]), minutes = int(ln[1]), seconds=int(ln[2]) )
    print(startdate)
    print(enddate)
    finished = str(enddate.month)+", "+str(enddate.day)+", "+str(enddate.year)+" "+str(enddate.hour)+":"+str(enddate.minute)+":"+str(enddate.second)
    print(finished)
    return render(request, 'front/contesttask.html',{'contestdetails':contestdetails, 'p':p, 'finished':finished})

def tasks(request,pk):

    con = Contest.objects.get(pk = pk)
    pks = con.problems
    pks = pks.split(",")
    probs = []
    for i in pks:
        if i != '':
            p1 = Problem.objects.get(pk = i)
            probs.append(p1)
    r = pk

    return render(request, 'front/tasks.html',{'probs':probs,'pks':pks,'r':r})


def cmp(a, b):
     return [c for c in a if c.isalpha()] == [c for c in b if c.isalpha()]

def whichproblem(x):

    list = ['A','B','C','D','E','F','H','I','J','K']

    return list[int(x)]

def Totalmarkproblem(x):

    list = ['tpb1','tpb2','tpb3','tpb4','tpb5','tpb6','tpb7','tpb8','tpb9','tpb10']

    return list[int(x)]


def contestproblem(request,pk1,pk2):



    details = Problem.objects.get(pk=pk2)
    language = ['Java','NodeJS','C','C++','PHP','Python 2','Python 3','Kotlin','GO Lang','C#']

    i = Contest.objects.get(pk=pk1)
    sdate = i.cbeginingdate
    sdate = sdate.split("-")
    day = sdate[2]
    year = sdate[0]
    month = sdate[1]

    if len(str(day)) == 1:
        day = '0' + str(day)
    if len(str(month)) == 1:
        month = '0' + str(month)

    stime = i.cbeginingtime
    stime = stime.split(":")

    if len(str(stime[0])) == 1:
        stime[0] = '0' + str(stime[0])
    if len(str(stime[1])) == 1:
        stime[1] = '0' + str(stime[1])
    p1 = day+"/"+month+"/"+year+" "+stime[0]+":"+stime[1]+":"+str(00)
    startdate = datetime.datetime.strptime(p1, '%d/%m/%Y %H:%M:%S')
    today = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    today = datetime.datetime.strptime(today,'%d/%m/%Y %H:%M:%S')
    #print(today)
    #print(startdate)
    diff = today - startdate
    diff = today - startdate
    if int(diff.days) < 0:
        return redirect('contesttask',pk=pk1)


    cleanr = re.compile(r'<[^>]+>')

    input = details.psinput
    input = re.sub(cleanr,'',input)
    output = details.psoutput
    output = re.sub(cleanr,'',output)
    input = input.split(";")
    output = output.split(";")

    if request.method == 'POST':

        #Checking if Finished...
        i = Contest.objects.get(pk=pk1)
        sdate = i.cbeginingdate
        sdate = sdate.split("-")
        day = sdate[2]
        year = sdate[0]
        month = sdate[1]

        if len(str(day)) == 1:
            day = '0' + str(day)
        if len(str(month)) == 1:
            month = '0' + str(month)

        stime = i.cbeginingtime
        stime = stime.split(":")

        if len(str(stime[0])) == 1:
            stime[0] = '0' + str(stime[0])
        if len(str(stime[1])) == 1:
            stime[1] = '0' + str(stime[1])
        p1 = day+"/"+month+"/"+year+" "+stime[0]+":"+stime[1]+":"+str(00)
        startdate = datetime.datetime.strptime(p1, '%d/%m/%Y %H:%M:%S')
        today = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        today = datetime.datetime.strptime(today,'%d/%m/%Y %H:%M:%S')
        #print(today)
        #print(startdate)
        diff = today - startdate

        ln = i.clength
        ln = ln.split(":")
        enddate = startdate + datetime.timedelta(hours=int(ln[0]), minutes = int(ln[1]), seconds=int(ln[2]) )

        finished = str(enddate.day)+"/"+str(enddate.month)+"/"+str(enddate.year)+" "+str(enddate.hour)+":"+str(enddate.minute)+":"+str(enddate.second)
        finished = datetime.datetime.strptime(finished, '%d/%m/%Y %H:%M:%S')
        #print(finished)
        diff1 = finished-today
        #print(diff)
        #print(diff1)
        if diff.days>=0 and diff1.days<0:
            return redirect('contesttask',pk=pk1)





        # checking if user in contest:
        uname = request.user.username
        allusers = Contest.objects.get(pk=pk1)
        print(allusers)
        cnt = allusers.contestants
        alluser = cnt.split(",")
        if uname not in alluser:
            x = cnt
            if len(alluser) != 0:
                x += ","+uname
            else:
                x = ""
                x = uname
            allusers.contestants = x
            allusers.save()

            #Creating a new table for a new user:
            b = Ranklist(user = uname,contestid=pk1)
            b.save()

        #Submissionid
        bb = Submission(user = uname, contestid = pk1)
        bb.save()
        subid = bb.submissionid




        lan = request.POST.get('language')
        code = request.POST.get('code')

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
        bb.problemid = pk2
        bb.save()




        pbn = 0
        prob = allusers.problems
        prob = prob.split(",")
        for i in prob:
            if i == pk2:
                #pbn += 1
                break
            else:
                pbn += 1
        spb = whichproblem(pbn)
        tpb = Totalmarkproblem(pbn)

        bb.problemtitle = spb
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
        usr = request.user.username
        pro = Profile.objects.get(uname = usr)
        rls = Ranklist.objects.get(user = uname , contestid = pk1)
        for i in range(0,len(p)):
            inp = p[i]
            out = q[i]
            cleanr = re.compile(r'<[^>]+>')
            inp = re.sub(cleanr,'',inp)
            out = re.sub(cleanr,'',out)
            print(inp)
            print(code)
            print(lan)
            print(ver)
            task = {"clientId": "827646b49b0d2e078eb637d28a3d4202", "clientSecret":"f81ec97b9f03ef577968c605fd1b53fe67a6b3e74bc64f3eb3435e45cb5f0779", "script": code , "stdin" : inp, "language" : lan, "versionIndex": ver}
            resp = requests.post("https://api.jdoodle.com/v1/execute", headers=headers, json = json.dumps(task))
            print(resp)
            resp = resp.json()
            #input
            print(resp)

            if resp['statusCode'] == 200:
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
                    print("i am here for memory")
                    bb.status = 'Syntex Error'
                    bb.save()
                    sub = pro.totalsub
                    sub += 1
                    pro.totalsub = sub
                    wa = pro.totalwa
                    wa += 1
                    pro.totalwa = wa
                    pro.save()
                    if pbn == 0:
                        x = rls.tpb1
                        x += 10
                        rls.tpb1 = x
                        rls.save()
                        #messages.info(request, "Syntex Error")
                        return redirect('submission', pk = pk1)
                    elif pbn == 1:
                        x = rsl.tpb2
                        x += 10
                        rls.tpb2 = x
                        rls.save()
                        #messages.info(request, "Syntex Error")
                        return redirect('submission', pk = pk1)
                    elif pbn == 2:
                        x = rsl.tpb3
                        x += 10
                        rls.tpb3 = x
                        rls.save()
                        #messages.info(request, "Syntex Error")
                        return redirect('submission', pk = pk1)
                    elif pbn == 3:
                        x = rsl.tpb4
                        x += 10
                        rls.tpb4 = x
                        rls.save()
                        return redirect('submission', pk = pk1)
                    elif pbn == 4:
                        x = rsl.tpb5
                        x += 10
                        rls.tpb5 = x
                        rls.save()
                        #messages.info(request, "Syntex Error")
                        return redirect('submission', pk = pk1)
                    elif pbn == 5:
                        x = rsl.tpb6
                        x += 10
                        rls.tpb6 = x
                        rls.save()
                        return redirect('submission', pk = pk1)
                    elif pbn == 6:
                        x = rsl.tpb7
                        x += 10
                        rls.tpb7 = x
                        rls.save()
                        return redirect('submission', pk = pk1)
                    elif pbn == 7:
                        x = rsl.tpb8
                        x += 10
                        rls.tpb8 = x
                        rls.save()
                        return redirect('submission', pk = pk1)
                    elif pbn == 8:
                        x = rsl.tpb9
                        x += 10
                        rls.tpb9 = x
                        rls.save()
                        return redirect('submission', pk = pk1)
                    elif pbn == 9:
                        x = rsl.tpb10
                        x += 10
                        rls.tpb10 = x
                        rls.save()

                        return redirect('submission', pk = pk1)
                    ac = False

                else:
                    if float(stl) <= gtl :
                        print("i am here 2")
                        if float(sml)<=gml :
                            print("i am here 3")
                            if cmp(op,out) == True:
                                print("i am here 4")
                                continue
                            else:
                                print("i am here wa")
                                sub = pro.totalsub
                                sub += 1
                                pro.totalsub = sub
                                wa = pro.totalwa
                                wa += 1
                                pro.totalwa = wa
                                pro.save()
                                bb.status = 'Worng Answer'
                                bb.save()
                                if pbn == 0:
                                    x = rls.tpb1
                                    x += 10
                                    rls.tpb1 = x
                                    rls.save()
                                    return redirect('submission', pk = pk1)
                                elif pbn == 1:

                                    x = rls.tpb2
                                    x += 10
                                    rls.tpb2 = x
                                    rls.save()
                                    return redirect('submission', pk = pk1)
                                elif pbn == 2:

                                    x = rls.tpb3
                                    x += 10
                                    rls.tpb3 = x
                                    rls.save()
                                    return redirect('submission', pk = pk1)
                                elif pbn == 3:

                                    x = rls.tpb4
                                    x += 10
                                    rls.tpb4 = x
                                    rls.save()
                                    return redirect('submission', pk = pk1)
                                elif pbn == 4:

                                    x = rls.tpb5
                                    x += 10
                                    rls.tpb5 = x
                                    rls.save()
                                    return redirect('submission', pk = pk1)
                                elif pbn == 5:

                                    x = rls.tpb6
                                    x += 10
                                    rls.tpb6 = x
                                    rls.save()
                                    return redirect('submission', pk = pk1)
                                elif pbn == 6:

                                    x = rls.tpb7
                                    x += 10
                                    rls.tpb7 = x
                                    rls.save()
                                    return redirect('submission', pk = pk1)
                                elif pbn == 7:

                                    x = rls.tpb8
                                    x += 10
                                    rls.tpb8 = x
                                    rls.save()
                                    return redirect('submission', pk = pk1)
                                elif pbn == 8:

                                    x = rls.tpb9
                                    x += 10
                                    rls.tpb9 = x
                                    rls.save()
                                    return redirect('submission', pk = pk1)
                                elif pbn == 9:

                                    x = rls.tpb10
                                    x += 10
                                    rls.tpb10 = x
                                    rls.save()
                                    return redirect('submission', pk = pk1)
                                ac = False
                                break
                        else:
                            print("i am here 6")
                            sub = pro.totalsub
                            sub += 1
                            pro.totalsub = sub
                            me = pro.totalme
                            me += 1
                            pro.totalme = me
                            pro.save()
                            bb.status = 'Memory Limit Exc.'
                            bb.save()
                            if pbn == 0:
                                x = rls.tpb1
                                x += 10
                                rls.tpb1 = x
                                rls.save()
                                return redirect('submission', pk = pk1)
                            elif pbn == 1:

                                x = rls.tpb2
                                x += 10
                                rls.tpb2 = x
                                rls.save()
                                return redirect('submission', pk = pk1)
                            elif pbn == 2:

                                x = rls.tpb3
                                x += 10
                                rls.tpb3 = x
                                rls.save()
                                return redirect('submission', pk = pk1)
                            elif pbn == 3:

                                x = rls.tpb4
                                x += 10
                                rls.tpb4 = x
                                rls.save()
                                return redirect('submission', pk = pk1)
                            elif pbn == 4:

                                x = rls.tpb5
                                x += 10
                                rls.tpb5 = x
                                rls.save()
                                return redirect('submission', pk = pk1)
                            elif pbn == 5:

                                x = rls.tpb6
                                x += 10
                                rls.tpb6 = x
                                rls.save()
                                return redirect('submission', pk = pk1)
                            elif pbn == 6:

                                x = rls.tpb7
                                x += 10
                                rls.tpb7 = x
                                rls.save()
                                return redirect('submission', pk = pk1)
                            elif pbn == 7:

                                x = rls.tpb8
                                x += 10
                                rls.tpb8 = x
                                rls.save()
                                return redirect('submission', pk = pk1)
                            elif pbn == 8:

                                x = rls.tpb9
                                x += 10
                                rls.tpb9 = x
                                rls.save()
                                return redirect('submission', pk = pk1)
                            elif pbn == 9:

                                x = rls.tpb10
                                x += 10
                                rls.tpb10 = x
                                rls.save()
                                return redirect('submission', pk = pk1)
                            ac = False
                            break
                    else:
                        print("i am here 9")
                        sub = pro.totalsub
                        sub += 1
                        pro.totalsub = sub
                        tl = pro.totaltle
                        tl += 1
                        pro.totaltle = tl
                        pro.save()
                        bb.status = 'Time Limit'
                        bb.save()
                        if pbn == 0:
                            x = rls.tpb1
                            x += 10
                            rls.tpb1 = x
                            rls.save()
                            return redirect('submission', pk = pk1)
                        elif pbn == 1:

                            x = rls.tpb2
                            x += 10
                            rls.tpb2 = x
                            rls.save()
                            return redirect('submission', pk = pk1)
                        elif pbn == 2:

                            x = rls.tpb3
                            x += 10
                            rls.tpb3 = x
                            rls.save()
                            return redirect('submission', pk = pk1)
                        elif pbn == 3:

                            x = rls.tpb4
                            x += 10
                            rls.tpb4 = x
                            rls.save()
                            return redirect('submission', pk = pk1)
                        elif pbn == 4:

                            x = rls.tpb5
                            x += 10
                            rls.tpb5 = x
                            rls.save()
                            return redirect('submission', pk = pk1)
                        elif pbn == 5:

                            x = rls.tpb6
                            x += 10
                            rls.tpb6 = x
                            rls.save()
                            return redirect('submission', pk = pk1)
                        elif pbn == 6:

                            x = rls.tpb7
                            x += 10
                            rls.tpb7 = x
                            rls.save()
                            return redirect('submission', pk = pk1)
                        elif pbn == 7:

                            x = rls.tpb8
                            x += 10
                            rls.tpb8 = x
                            rls.save()
                            return redirect('submission', pk = pk1)
                        elif pbn == 8:

                            x = rls.tpb9
                            x += 10
                            rls.tpb9 = x
                            rls.save()
                            return redirect('submission', pk = pk1)
                        elif pbn == 9:

                            x = rls.tpb10
                            x += 10
                            rls.tpb10 = x
                            rls.save()
                            return redirect('submission', pk = pk1)
                        ac = False
                        break

            else:
                print("i am here 10")
                bb.status = 'Wrong Answer'
                bb.save()
                if pbn == 0:
                    x = rls.tpb1
                    x += 10
                    rls.tpb1 = x
                    rls.save()
                    return redirect('submission', pk = pk1)
                elif pbn == 1:

                    x = rls.tpb2
                    x += 10
                    rls.tpb2 = x
                    rls.save()
                    return redirect('submission', pk = pk1)
                elif pbn == 2:

                    x = rls.tpb3
                    x += 10
                    rls.tpb3 = x
                    rls.save()
                    return redirect('submission', pk = pk1)
                elif pbn == 3:

                    x = rls.tpb4
                    x += 10
                    rls.tpb4 = x
                    rls.save()
                    return redirect('submission', pk = pk1)
                elif pbn == 4:

                    x = rls.tpb5
                    x += 10
                    rls.tpb5 = x
                    rls.save()
                    return redirect('submission', pk = pk1)
                elif pbn == 5:

                    x = rls.tpb6
                    x += 10
                    rls.tpb6 = x
                    rls.save()
                    return redirect('submission', pk = pk1)
                elif pbn == 6:

                    x = rls.tpb7
                    x += 10
                    rls.tpb7 = x
                    rls.save()
                    return redirect('submission', pk = pk1)
                elif pbn == 7:

                    x = rls.tpb8
                    x += 10
                    rls.tpb8 = x
                    rls.save()
                    return redirect('submission', pk = pk1)
                elif pbn == 8:

                    x = rls.tpb9
                    x += 10
                    rls.tpb9 = x
                    rls.save()
                    return redirect('submission', pk = pk1)
                elif pbn == 9:

                    x = rls.tpb10
                    x += 10
                    rls.tpb10 = x
                    rls.save()
                    return redirect('submission', pk = pk1)
                ac = False
                messages.info(request, "Rewrite Code with Correct Formate or select language correctly")
                return redirect('contestproblem', pk1=pk1, pk2=pk2)

        if ac == True:
            print("i am here 11")
            bb.status = 'Accepted'
            bb.save()
            sub = pro.totalsub
            sub += 1
            pro.totalsub = sub
            ac = pro.totalac
            ac += 1
            pro.totalac = ac

            if pbn == 0 and rls.spb1 == False:
                rls.spb1 = True
                x = rls.tpb1
                x += 100
                rls.tpb1 = x
                y = rls.totalac
                y += 1
                rls.totalac = y
                z = rls.totalpoint
                z += x
                rls.totalpoint = z
                rls.save()
                return redirect('submission', pk = pk1)
            elif pbn == 1 and rls.spb2 == False:
                rls.spb2 = True
                x = rls.tpb2
                x += 100
                rls.tpb2 = x
                y = rls.totalac
                y += 1
                rls.totalac = y
                z = rls.totalpoint
                z += x
                rls.totalpoint = z
                rls.save()
                return redirect('submission', pk = pk1)
            elif pbn == 2 and rls.spb3 == False:
                rls.spb3 = True
                x = rls.tpb3
                x += 100
                rls.tpb3 = x
                y = rls.totalac
                y += 1
                rls.totalac = y
                z = rls.totalpoint
                z += x
                rls.totalpoint = z
                rls.save()
                return redirect('submission', pk = pk1)
            elif pbn == 3 and rls.spb4 == False:
                rls.spb4 = True
                x = rls.tpb4
                x += 100
                rls.tpb4 = x
                y = rls.totalac
                y += 1
                rls.totalac = y
                z = rls.totalpoint
                z += x
                rls.totalpoint = z
                rls.save()
                return redirect('submission', pk = pk1)
            elif pbn == 4 and rls.spb5 == False:
                rls.spb5 = True
                x = rls.tpb5
                x += 100
                rls.tpb5 = x
                y = rls.totalac
                y += 1
                rls.totalac = y
                z = rls.totalpoint
                z += x
                rls.totalpoint = z
                rls.save()
                return redirect('submission', pk = pk1)
            elif pbn == 5 and rls.spb6 == False:
                rls.spb6 = True
                x = rls.tpb6
                x += 100
                rls.tpb6 = x
                y = rls.totalac
                y += 1
                rls.totalac = y
                z = rls.totalpoint
                z += x
                rls.totalpoint = z
                rls.save()
                return redirect('submission', pk = pk1)
            elif pbn == 6 and rls.spb7 == False:
                rls.spb7 = True
                x = rls.tpb7
                x += 100
                rls.tpb7 = x
                y = rls.totalac
                y += 1
                rls.totalac = y
                z = rls.totalpoint
                z += x
                rls.totalpoint = z
                rls.save()
                return redirect('submission', pk = pk1)
            elif pbn == 7 and rls.spb8 == False:
                rls.spb8 = True
                x = rls.tpb8
                x += 100
                rls.tpb8 = x
                y = rls.totalac
                y += 1
                rls.totalac = y
                z = rls.totalpoint
                z += x
                rls.totalpoint = z
                rls.save()
                return redirect('submission', pk = pk1)
            elif pbn == 8 and rls.spb9 == False:
                rls.spb9 = True
                x = rls.tpb9
                x += 100
                rls.tpb9 = x
                y = rls.totalac
                y += 1
                rls.totalac = y
                z = rls.totalpoint
                z += x
                rls.totalpoint = z
                rls.save()
                return redirect('submission', pk = pk1)
            elif pbn == 9 and rls.spb10 == False:
                rls.spb10 = True
                x = rls.tpb10
                x += 100
                rls.tpb10 = x
                y = rls.totalac
                y += 1
                rls.totalac = y
                z = rls.totalpoint
                z += x
                rls.totalpoint = z
                rls.save()
                return redirect('submission', pk = pk1)



    return render(request, 'front/contestproblem.html',{'details':details,'language':language,'r':pk1,'input':input,'output':output})


def ranklist(request,pk):

    users = Ranklist.objects.filter(contestid = pk).order_by('-totalac', 'totalpoint')
    print(users)
    contest = Contest.objects.get(pk=pk)

    s = 'A'
    dic = {}
    probs = contest.problems
    x = 0
    probs = probs.split(",")
    for i in probs:
        if i!= "":
            y = chr(ord(s)+x)
            dic[y] = i
            x += 1
    print(dic)
    r = pk

    sz = len(dic)
    print(sz)

    return render(request, 'front/ranklist.html',{'users':users,'contest':contest,'dic':dic,'r':r,'sz':sz})


def submission(request,pk):

    sub = Submission.objects.filter(contestid = pk, user = request.user.username).order_by('-pk')
    return render(request, 'front/submission.html',{'sub':sub,'r':pk})

def viewsubmittedcode(request,pk):

    code = Submission.objects.get(pk=pk)

    return render(request, 'front/viewsubmittedcode.html',{'code':code})
