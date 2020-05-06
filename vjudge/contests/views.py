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
#from contests.models import *

# Create your views here.

def contestpage(request):

    contests = Contest.objects.all()
    return render(request, 'front/contestlist.html', {'contests' : contests})

def createcontestpage(request):

    if request.method == 'POST':

        title = request.POST.get('ctitle')
        description = request.POST.get('cdescription')
        beginingdate = request.POST.get('cbeginingdate')
        beginingtime = request.POST.get('cbeginingtime')
        length = request.POST.get('clength')
        password = request.POST.get('cpassword')
        b = Contest(ctitle = title , cbeginingdate = beginingdate, cdescription = description, cbeginingtime = beginingtime, clength = length, cpassword = password)
        b.save()
        print(title)

        return redirect('contest')

    return render(request, 'front/createcontest.html')

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
               thour = now.year
               tmin = now.minute
               if len(str(thour)) == 1:
                   tday = '0' + str(tday)
               if len(str(tmonth)) == 1:
                   tmonth = '0' + str(tmonth)

               if (int(tyear) > int(year)) or (int(tmonth) > int(month) and int(tyear) == int(year)) or (int(tday) >= int(day) and int(tmonth) == int(month) and int(tyear) == int(year)):
                    print(1)
                    if (str(thour) > stime[0]) or (str(thour) == stime[0] and str(tmin) >= stime[1]):
                        return redirect('tasks', pk=contestdetails.pk)
               else:
                   messages.info(request, "Contest Not started Yet")
                   return redirect('contesttask', pk=contestdetails.pk)

    p = month+", "+day+", "+year+" "+stime[0]+":"+stime[1]+":"+str(00)
    #print(p)
    return render(request, 'front/contesttask.html',{'contestdetails':contestdetails, 'p':p})

def tasks(request,pk):

    return render(request, 'front/tasks.html')
