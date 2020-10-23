from django.forms import ModelForm, Select, SelectDateWidget
from .models import Appointment
from django.forms.widgets import SelectMultiple
from django import forms
import datetime


class DateInput(forms.DateInput):
    input_type = 'date'


class AppointmentForm(ModelForm):

    class Meta:
        model = Appointment
        fields = '__all__'
        labels = {
            'date': "Date",
            'timeslot': "Time Slot",
            'servicetype': "Service Type",

        }
        help_text = {
            'date': "",
            'timeslot': "",
            'servicetype': "",
        }
        widgets = {
            'date': DateInput(attrs={'min': datetime.datetime.now().strftime("%d-%m-%Y"), 'class': 'form-control',
                                     'placeholder': ''}),
            'timeslot': Select(attrs={'class': 'form-control'}),
            'servicetype': Select(attrs={'class': 'form-control'})

        }

    # def clean_timeslot(self):
    #     data = self.cleaned_data('timeslot')
    #     return data.spit(',')

    def __init__(self, choicelist, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['timeslot'].queryset = choicelist
        self.fields['date'].widget.attrs['style'] = 'width:400px; height:40px; color: blue'
        self.fields['timeslot'].widget.attrs['style'] = 'width:400px; height:40px;'
        self.fields['servicetype'].widget.attrs['style'] = 'width:400px; height:40px;'


class FindAppointmentForm(forms.Form):
    date = forms.DateField(label="Date");
