from django import forms

class ContactForm(forms.Form):
    position = forms.CharField(max_length=250)
    companyId = forms.IntegerField()
    userId = forms.IntegerField()

   
