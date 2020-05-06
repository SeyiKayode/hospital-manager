from datetime import datetime
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Case
from home.context_processors import hasGroup
from stock.models import Items
from bill.models import Bill
from appointment.models import Appointment
# Create your views here.


def generate(request):
    if hasGroup(request.user, 'receptionist'):
        c = {}
        c.update(csrf(request))
        c['patients'] = User.objects.filter(groups__name='patient')
        return render(request, 'case/generate.html', c)
    else:
        messages.warning(request, 'Access Denied')
        return HttpResponseRedirect('/')


def doGenerate(request):
    if hasGroup(request.user, 'receptionist'):
        try:
            patient = User.objects.get(username=request.POST.get('patient', ''))
            description = request.POST.get('description', '')
            filled_date = datetime.now()
            c = Case(patient=patient, receptionist=request.user, description=description, filled_date=filled_date)
            c.save()
            item = Items.objects.get(item_name='Consulting Charges')
            quantity = 1
            bill_date = datetime.now()
            bill_details = 'Basic Consulting Charges'
            amount = item.sell_price * quantity
            b = Bill(case=c, item=item, quantity=quantity, bill_date=bill_date, bill_details=bill_details, amount=amount)
            b.save()
            messages.success(request, 'Successfully generated Case')
            return HttpResponseRedirect('/appointments/book')
        except ObjectDoesNotExist:
            messages.info(request, 'No Such User')
            return HttpResponseRedirect('/case/generate')
    else:
        messages.info(request, 'Access Denied')
        return HttpResponseRedirect('/')


def view(request):
    c = {}
    user = request.user
    cases = None
    if hasGroup(user, 'receptionist'):
        cases = Case.objects.all()
    elif hasGroup(user, 'patient'):
        cases = Case.objects.filter(patient=user)
    elif hasGroup(user, 'doctor'):
        c['isDoctor'] = True
        cases = [appointment.case for appointment in Appointment.objects.filter(doctor=user)]

    opened = []
    closed = []
    for ca in cases:
        if ca.closed_date:
            closed.append(ca)
        else:
            opened.append(ca)
    c['openedCases'] = opened
    c['closedCases'] = closed
    return render(request, 'case/view.html', c)


def close(request, id):
    user = request.user
    if hasGroup(user, 'doctor'):
        c = Case.objects.get(id=id)
        c.closed_date = datetime.now()
        c.save()
        messages.info(request, 'Successfully closed Case')
        return HttpResponseRedirect('/case')
    else:
        messages.warning(request, 'Access Denied')
        return HttpResponseRedirect('/')


def delete(request, id):
    user = request.user
    if hasGroup(user, 'receptionist'):
        c = Case.objects.get(id=id)
        c.delete()
        messages.info(request, 'Successfully deleted Case')
        return HttpResponseRedirect('/case')
    else:
        messages.warning(request, 'Access Denied')
        return HttpResponseRedirect('/')





























































