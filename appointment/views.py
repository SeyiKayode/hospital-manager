from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from home.context_processors import hasGroup
from case.models import Case
from .models import Appointment
# Create your views here.


def book(request):
    user = request.user
    if hasGroup(user, 'receptionist'):
        c = {}
        c.update(csrf(request))
        c['patients'] = User.objects.filter(groups__name='patient')
        c['doctors'] = User.objects.filter(groups__name='doctor')
        c['cases'] = Case.objects.all()
        return render(request, 'appointment/book_appointment.html', c)
    else:
        messages.warning(request, 'Access Denied')
        return HttpResponseRedirect('/')


def doBook(request):
    user = request.user
    if hasGroup(user, 'receptionist'):
        patient = User.objects.get(username=request.POST.get('patient', ''))
        doctor = User.objects.get(username=request.POST.get('doctor', ''))
        c = Case.objects.get(pk=int(request.POST.get('case', '')))
        appointment_time = request.POST.get('appointment_date') + 'T' + request.POST.get('appointment_time')
        appointment_time = datetime(*[int(v) for v in appointment_time.replace('T', '-').replace(':', '-').split('-')])
        appointment = Appointment(patient=patient, doctor=doctor, case=c, receptionist=user,
                                  appointment_time=appointment_time)
        appointment.save()
        messages.info(request, 'Appointment Successfully Booked')
    else:
        messages.warning(request, 'Access Denied')
    return HttpResponseRedirect('/appointments/')


def view(request):
    c = {}
    user = request.user
    if hasGroup(user, 'receptionist'):
        c['isReceptionist'] = True
        c['appointments'] = Appointment.objects.filter(
            appointment_time__gte=timezone.now()).order_by('appointment_time')
    elif hasGroup(user, 'patient'):
        c['appointments'] = Appointment.objects.filter(
            patient=user, appointment_time__gte=timezone.now()).order_by('appointment_time')
    elif hasGroup(user, 'doctor'):
        c['appointments'] = Appointment.objects.filter(
            doctor=user, appointment_time__gte=timezone.now()).order_by('appointment_time')
    else:
        messages.warning(request, 'Access Denied')
        return HttpResponseRedirect('/')
    return render(request, 'appointment/view_all.html', c)


def changeAppointment(request, id):
    user = request.user
    if hasGroup(user, 'receptionist'):
        c = {'appointment': Appointment.objects.get(pk=id), 'doctors': User.objects.filter(groups__name='doctor')}
        c.update(csrf(request))
        return render(request, 'appointment/change.html', c)
    else:
        messages.warning(request, 'Access Denied')
        return HttpResponseRedirect('/')


def doChange(request):
    user = request.user
    if hasGroup(user, 'receptionist'):
        appointment = Appointment.objects.get(pk=int(request.POST.get('id')))
        appointment.doctor = User.objects.get(username=request.POST.get('doctor', ''))
        appointment_time = request.POST.get('appointment_date') + 'T' + request.POST.get('appointment_time')
        appointment_time = datetime(*[int(v) for v in appointment_time.replace('T', '-').replace(':', '-').split('-')])
        appointment.appointment_time = appointment_time
        appointment.receptionist = request.user
        appointment.save()
        messages.info(request, 'Appointment Successfully Changed')
        return HttpResponseRedirect('/appointments')
    else:
        messages.warning(request, 'Access Denied')
        return HttpResponseRedirect('/')


def delete(request, id):
    user = request.user
    if hasGroup(user, 'receptionist'):
        a = Appointment.objects.get(id=id)
        a.delete()
        messages.info(request, 'Appointment Successfully deleted')
        return HttpResponseRedirect('/appointments')
    else:
        messages.warning(request, 'Access Denied')
        return HttpResponseRedirect('/')


































































