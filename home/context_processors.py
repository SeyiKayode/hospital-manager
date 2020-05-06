from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.http import HttpResponseRedirect


def hasGroup(user, groupName):
    try:
        group = Group.objects.get(name=groupName)
        if group in user.groups.all():
            return True
        else:
            return False
    except:
        return False


def menu_processor(request):
    menu = {}
    user = request.user
    if hasGroup(user, 'doctor'):
        menu['Appointments'] = '/appointments'
        menu['Cases'] = '/case'
        menu['Reports'] = '/reports'
    elif hasGroup(user, 'patient'):
        menu['Reports'] = '/reports'
        menu['Appointments'] = '/appointments'
        menu['Medication'] = '/bill/medicines'
        menu['Bills'] = '/bill'
        menu['Cases'] = '/case'
    elif hasGroup(user, 'receptionist'):
        menu['New Patient'] = '/profile/register'
        menu['Manage Appointments'] = '/appointments'
        menu['New Appointment'] = '/appointments/book'
        menu['Bills'] = '/bill'
        menu['Cases'] = '/case'
        menu['Generate Case'] = '/case/generate'
    elif hasGroup(user, 'lab_attendant'):
        menu['Reports'] = '/reports'
        menu['Generate Report'] = '/reports/generate'
    return {'menu': menu}




















