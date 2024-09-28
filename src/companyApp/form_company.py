from django import forms

class CompanyForm(forms.Form):
    status = forms.CharField(max_length=50, required=False)  # Allow status to be optional
    structureId = forms.IntegerField(min_value=1)  # Ensure structureId is a positive integer
