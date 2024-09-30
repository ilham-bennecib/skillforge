from django import forms

class CfaEmployeeContactForm(forms.Form):
    cfaemployeeId = forms.IntegerField()
    contactId = forms.IntegerField()
    exchange = forms.CharField(widget=forms.Textarea)  # Champs pour l'échange
