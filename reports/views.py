from datetime import datetime
from django.shortcuts import render
from django.contrib import messages
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from home.context_processors import hasGroup
from case.models import Case
from .models import Report
# Create your views here.


def generate(request):
    user = request.user
    if hasGroup(user, 'lab_attendant'):
        c = {}
        c.update(csrf(request))
        c['cases'] = Case.objects.all()
        return render(request, 'report/generate.html', c)
    else:
        messages.warning(request, 'Access Denied')
        return HttpResponseRedirect('/')


def doGenerate(request):
    user = request.user
    if hasGroup(user, 'lab_attendant'):
        c = Case.objects.get(id=request.POST.get('case'))
        description = request.POST.get('description')
        generated_date = datetime.now()
        report = Report(case=c, lab_attendant=user, description=description, generated_date=generated_date)
        report.save()
        messages.info(request, 'Report successfully generated')
        return HttpResponseRedirect('/reports')
    else:
        messages.warning(request, 'Access Denied')
        return HttpResponseRedirect('/')


def view(request):
    c = {}
    user = request.user
    if hasGroup(user, 'lab_attendant'):
        c['isLabAttendant'] = True
        c['reports'] = Report.objects.filter(lab_attendant=user)
    elif hasGroup(user, 'doctor'):
        c['reports'] = Report.objects.all()
    elif hasGroup(user, 'patient'):
        c['reports'] = [report for report in Report.objects.all() if report.case.patient == user]
    else:
        messages.warning(request, 'Access Denied')
        return HttpResponseRedirect('/')
    return render(request, 'report/view.html', c)


def delete(request, id):
    user = request.user
    if hasGroup(user, 'lab_attendant'):
        r = Report.objects.get(id=id)
        r.delete()
    return HttpResponseRedirect('/reports')











































