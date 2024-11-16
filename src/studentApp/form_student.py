from django import forms

class StudentForm(forms.Form):

    companyId = forms.IntegerField(min_value=1)  
    sessionId = forms.IntegerField(min_value=1)  
    candidateId = forms.IntegerField(min_value=1)  
