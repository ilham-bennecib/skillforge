from django import forms

class EventForm(forms.Form):
    title = forms.CharField(max_length=250)
    description = forms.CharField(widget=forms.Textarea)
    date = forms.DateField()
    startTime = forms.TimeField()
    endTime = forms.TimeField()
    cfaemployeeId = forms.IntegerField()
