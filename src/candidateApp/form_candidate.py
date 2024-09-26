from django import forms

class CandidateForm(forms.Form):
    last_diploma = forms.CharField(max_length=250)
    date_of_birth = forms.CharField(max_length=250)
    address = forms.CharField(max_length=250)
   
