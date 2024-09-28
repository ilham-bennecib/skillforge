from django import forms

class FieldForm(forms.Form):
    name = forms.CharField(max_length=250)
