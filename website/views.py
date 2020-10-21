from django.shortcuts import render, redirect
from django.http import HttpResponse
from .form import *
from .models import *
import datetime


# Create your views here.


def check_appoinment_form_date(date, timeslot):
    date_time = date.strftime("%Y-%m-%d")
    selected_date = datetime.datetime.strptime(date_time, '%Y-%m-%d')
    week_day = date.weekday()
    today = datetime.datetime.today()
    is_slot_booked = Appointment.objects.filter(date=date, timeslot=timeslot).exists()

    if selected_date < today:
        return "The date can not be from past."
    elif is_slot_booked:
        return "Sorry, The slot has been taken."
    elif week_day == 4:
        return "We don't have any service in that day."
    else:
        return None


def search_appointment_date_checker(date):
    selected_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    weekday = selected_date.weekday()
    today = datetime.datetime.today() - datetime.timedelta(days=1)
    print(selected_date, today)
    if selected_date < today:
        return "The date can not be from past."
    elif weekday == 4:
        return "We don't have any service in this day."
    else:
        return None


def main_page(request):
    service_types = Appointment._meta.get_field('servicetype').choices
    timeslot = Appointment._meta.get_field('timeslot').choices
    form = AppointmentForm(choicelist=timeslot)

    service_list = []
    for service in service_types:
        service_list.append(service[1])

    # Logic for set appointment form
    if request.method == "POST":
        if 'set-appointment' in request.POST:
            form = AppointmentForm(timeslot, request.POST)
            form.is_valid()
            date = form.cleaned_data['date']
            timeslot = form.cleaned_data['timeslot']

            # The date can not be from past
            message = check_appoinment_form_date(date, timeslot)
            if message:
                context = {
                    'appointment_error': message,
                    'form': form,
                }
                return render(request, 'website/main_page.html', context)
            else:
                if form.is_valid():
                    appointment = form.save()
                    # Checking if the day if full
                    timeslot_count = Appointment.objects.filter(date=date).count()
                    print(timeslot_count)
                    if timeslot_count >= 20:  # day is full. so update the dayfulfilled databse
                        DateFulfilled(date=date, isFull=True).save()

                    context = {
                        'appointment': appointment,
                    }
                    return render(request, 'website/appointment_page.html', context)

        # Logic for find appointment form
        if 'find-appointment' in request.POST:
            if request.POST.get('date'):
                date = request.POST.get('date')
                message = search_appointment_date_checker(date)

                if message:
                    context = {
                        'find_appointment_error': message,
                        'form': form,
                    }
                    return render(request, 'website/main_page.html', context)
                else:
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

    context = {
        'form': form,
    }
    return render(request, 'website/main_page.html', context)


def about_page(request):
    return render(request, 'website/about_page.html')


def appointment_page(request):
    context = {
        'appointment': None,
    }
    return render(request, 'website/appointment_page.html', context)


def recommendation_page_date_checker(date):
    selected_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    weekday = selected_date.weekday()
    today = datetime.datetime.today() - datetime.timedelta(days=1)
    print(selected_date, today)
    if selected_date < today:
        return "The date can not be from past."
    elif weekday == 4:
        return "We don't have any service in this day."
    else:
        return None


def recommendation_page(request):
    timeslot = Appointment._meta.get_field('timeslot').choices
    if request.method == "POST":
        if request.POST.get('date'):
            date = request.POST.get('date')
            message = recommendation_page_date_checker(date)
            if message:
                context = {
                    'find_appointment_error': message,
                }
                return render(request, 'website/recommendation.html', context)
            else:
                selected_date = datetime.datetime.strptime(date, '%Y-%m-%d')
                is_fulfilled = DateFulfilled.objects.filter(date=selected_date).exists()
                if not is_fulfilled:
                    booked_timeslot = Appointment.objects.filter(date=selected_date).values('timeslot')
                    total_timeslot = {}
                    for time in timeslot:
                        total_timeslot[time[0]] = time[1]
                    filled_slots = []

                    for service in booked_timeslot:
                        filled_slots.append(total_timeslot[service['timeslot']])
                        # slots.append(service[1])

                    avaliable_slot = [ele for ele in total_timeslot.values() if ele not in filled_slots]
                    context = {
                        'timeslots': avaliable_slot,
                        'searched_date': date,
                    }
                    return render(request, 'website/recommendation.html', context)
                else:
                    selected_date = datetime.datetime.strptime(date, '%Y-%m-%d')
                    latest_full_day = DateFulfilled.objects.order_by('date').first()
                    latest_full_date = latest_full_day.date + datetime.timedelta(days=1)
                    booked_timeslot = Appointment.objects.filter(date=latest_full_date).values('timeslot')
                    total_timeslot = {}
                    for time in timeslot:
                        total_timeslot[time[0]] = time[1]
                    filled_slots = []

                    for service in booked_timeslot:
                        filled_slots.append(total_timeslot[service['timeslot']])
                        # slots.append(service[1])

                    avaliable_slot = [ele for ele in total_timeslot.values() if ele not in filled_slots]
                    context = {
                        'timeslots': avaliable_slot,
                        'searched_date': latest_full_date,
                        'searched_date_not_found': "Sorry this day is full. But we recommend you nearest time. Thank "
                                                   "you. "
                    }
                    return render(request, 'website/recommendation.html', context)


    return render(request, 'website/recommendation.html')
