from django.db import models


# Create your models here.


class TimeSlot(models.Model):
    name = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    SERVICES = (
        ('service1', 'Service-1'),
        ('service2', 'Service-2'),
        ('service3', 'Service-3'),
        ('service4', 'Service-4'),
        ('service5', 'Service-5'),
    )

    TIMESLOTS = (
        ('a', "9:00 am - 9:30 am"),
        ('b', "9:31 am - 10:00 am"),
        ('c', "10:01 am - 10:30 am"),
        ('d', "10:31 am - 11:00 am"),
        ('e', "11:01 am - 11:30 am"),
        ('f', "11:31 am - 12:00 pm"),
        ('g', "12:01 pm - 12:30 pm"),
        ('h', "12:31 pm - 1:00 pm"),
        ('i', "1:01 pm - 1:30 pm"),
        ('j', "1:31 pm - 2:00 pm"),
        ('k', "2:01 pm - 2:30 pm"),
        ('l', "2:31 pm - 3:00 pm"),
        ('m', "3:01 pm - 3:30 pm"),
        ('n', "	3:31 pm - 4:00 pm"),
        ('o', "4:01 pm - 4:30 pm"),
        ('p', "4:31 pm - 5:00 pm"),
        ('q', "	5:01 pm - 5:30 pm"),
        ('r', "	5:31 pm - 6:00 pm"),
        ('s', "	6:01 pm - 6:30 pm"),
        ('t', "6:31 pm - 7:00 pm")

    )
    date = models.DateField(blank=False)
    timeslot = models.CharField(max_length=30, choices=TIMESLOTS)
    servicetype = models.CharField(max_length=20, choices=SERVICES)

    def __str__(self):
        return self.date.__str__() + "  " + self.servicetype
