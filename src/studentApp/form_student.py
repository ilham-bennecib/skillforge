from django import forms

class StudentForm(forms.Form):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)  
    companyId = forms.IntegerField(min_value=1)  
    sessionId = forms.IntegerField(min_value=1)  
    candidateId = forms.IntegerField(min_value=1)  
