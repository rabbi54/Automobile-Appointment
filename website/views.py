from django.shortcuts import render, redirect
from django.http import HttpResponse
from .form import *
from .models import *
import datetime


# Create your views here.

def main_page(request):
    service_types = Appointment._meta.get_field('servicetype').choices
    timeslot = Appointment._meta.get_field('timeslot').choices
    form = AppointmentForm(choicelist=timeslot)

    service_list = []
    for service in service_types:
        service_list.append(service[1])

    if request.method == "POST":
        if 'set-appointment' in request.POST:
            form = AppointmentForm(timeslot, request.POST)
            form.is_valid()
            date = form.cleaned_data['date']
            if datetime.datetime.strptime(str(date), '%Y-%m-%d') > datetime.datetime.today():
                if form.is_valid():
                    appointment = form.save();
                    print(appointment)
                    context = {
                        'appointment': appointment,
                    }
                    return render(request, 'website/appointment_page.html', context)
            else:
                context = {
                    'appointment_error': "Date can not be in the past",
                    'form': form,
                }
                return render(request, 'website/main_page.html', context)

        if 'find-appointment' in request.POST:
            if request.POST.get('date'):
                date = request.POST.get('date');
                if datetime.datetime.strptime(date, '%Y-%m-%d') > datetime.datetime.today():
                    x = datetime.datetime.strptime(date, '%Y-%m-%d')
                    booked_timeslot = Appointment.objects.filter(date=x).values('timeslot')
                    total_timeslot = {}
                    for time in timeslot:
                        total_timeslot[time[0]] = time[1]
                    print(booked_timeslot)
                    filled_slots = []

                    for service in booked_timeslot:
                        filled_slots.append(total_timeslot[service['timeslot']])
                        # slots.append(service[1])

                    avaliable_slot = [ele for ele in total_timeslot.values() if ele not in filled_slots]
                    context = {
                        'form': form,
                        'service_types': service_list,
                        'timeslots': avaliable_slot,
                        'searched_date': date,
                    }
                    return render(request, 'website/main_page.html', context)
                else:
                    context = {
                        'find_appointment_error': "Date can not be in the past",
                        'form': form,
                    }
                    return render(request, 'website/main_page.html', context)

    context = {
        'form': form,
        # 'service_types': service_list,
        # 'timeslots': timeslot,
    }
    return render(request, 'website/main_page.html', context)


def about_page(request):
    return render(request, 'website/about_page.html')


def appointment_page(request):
    context = {
        'appointment': None,
    }
    return render(request, 'website/appointment_page.html', context)
