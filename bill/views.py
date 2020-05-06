from datetime import datetime
from django.shortcuts import render
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from home.context_processors import hasGroup
from stock.models import Items
from case.models import Case
from .models import Bill


# Create your views here.


def generate(request, case_id):
    if hasGroup(request.user, 'doctor'):
        c = {}
        c.update(csrf(request))
        c['case'] = Case.objects.get(id=int(case_id))
        c['items'] = Items.objects.all()
        return render(request, 'bill/generate.html', c)
    else:
        messages.warning(request, 'Access Denied')
        return HttpResponseRedirect('/')


def doGenerate(request):
    if hasGroup(request.user, 'doctor'):
        c = Case.objects.get(id=request.POST.get('case', ''))
        item = Items.objects.get(id=request.POST.get('item', ''))
        quantity = int(request.POST.get('quantity', ''))
        bill_date = timezone.now()
        bill_details = request.POST.get('description', '')
        amount = item.sell_price * quantity
        b = Bill(case=c, item=item, quantity=quantity, bill_details=bill_details, bill_date=bill_date, amount=amount)
        b.save()
        messages.info(request, 'Successfully added Medicine')
        return HttpResponseRedirect('/case/')
    else:
        messages.warning(request, 'Access Denied')
        return HttpResponseRedirect('/')


def view(request):
    c = {}
    c.update(csrf(request))
    if hasGroup(request.user, 'patient'):
        c['bills'] = []
        c['isPatient'] = True
        for cases in Case.objects.filter(patient=request.user):
            c['bills'].extend(list(Bill.objects.filter(case=cases)))
    elif hasGroup(request.user, 'receptionist'):
        id = request.POST.get('patient', '')
        if id == '':
            c['selectPatient'] = True
            c['patients'] = User.objects.filter(groups__name='patient')
            return render(request, 'bill/view_bill.html', c)
        else:
            c['bills'] = []
            for cases in Case.objects.filter(patient=User(id=id)):
                c['bills'].extend(list(Bill.objects.filter(case=cases)))
    else:
        messages.warning(request, 'Access Denied')
        return HttpResponseRedirect('/')

    bills = c['bills']
    c['paidBills'] = []
    c['pendingBills'] = []
    for b in bills:
        if b.is_paid:
            c['paidBills'].append(b)
        else:
            c['pendingBills'].append(b)
    return render(request, 'bill/view_bill.html', c)


def viewMedicine(request):
    c = {}
    if hasGroup(request.user, 'patient'):
        c['bills'] = []
        c['isPatient'] = True
        for cases in Case.objects.filter(patient=request.user):
            c['bills'].extend(list(Bill.objects.filter(case=cases)))
        return render(request, 'bill/medicines.html', c)
    else:
        messages.warning(request, 'Access Denied')
        return HttpResponseRedirect('/')


def pay(request):
    user = request.user
    if hasGroup(user, 'receptionist'):
        ids = request.POST.getlist('ids', '123')
        if type(ids) == type([]):
            for id in ids:
                b = Bill.objects.get(id=int(id))
                b.is_paid = True
                b.save()
        else:
            b = Bill.objects.get(id=int(ids))
            b.is_paid = True
            b.save()
        messages.info(request, 'Bill paid Successfully')
        return HttpResponseRedirect('/bill/')
    else:
        messages.warning(request, 'Access Denied')
        return HttpResponseRedirect('/')


def delete(request, id):
    user = request.user
    if hasGroup(user, 'receptionist'):
        b = Bill.objects.get(id=id)
        b.delete()
        messages.info(request, 'Bill has been deleted')
        return HttpResponseRedirect('/bill/')
    else:
        messages.warning(request, 'Access Denied')
        return HttpResponseRedirect('/')



















