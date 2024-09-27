from django import forms

class StructureForm(forms.Form):
    name = forms.CharField(max_length=250)
    address = forms.CharField(max_length=500, required=False)
    siret = forms.CharField(max_length=20, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    directory = forms.CharField(max_length=250)
    fieldId = forms.IntegerField()  # Use 'fieldId' to match the database field
