from django import forms

class CfaEmployeeForm(forms.Form):
    position = forms.CharField(max_length=250)
    matricule = forms.IntegerField()
    structureId = forms.IntegerField()
    userId = forms.IntegerField()  # Ensures userId validation is handled correctly
