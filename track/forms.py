from django import forms
from .models import TimeEntry, Client, Worker


class TimeEntryForm(forms.ModelForm):
    class Meta:
        model = TimeEntry
        fields = ['client', 'worker', 'start_time', 'end_time', 'description', 'date']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class TimeEntryFilterForm(forms.Form):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), required=False)
    worker = forms.ModelChoiceField(queryset=Worker.objects.all(), required=False)
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    invoice_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
