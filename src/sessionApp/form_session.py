from django import forms

class SessionForm(forms.Form):
    name = forms.CharField(max_length=250)
    referent = forms.IntegerField()
    tutor = forms.IntegerField()
    trainingId = forms.IntegerField()
