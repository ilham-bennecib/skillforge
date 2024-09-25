from django import forms

class UserForm(forms.Form):
    last_name = forms.CharField(max_length=250)
    first_name = forms.CharField(max_length=250)
    email = forms.EmailField()
    phone = forms.CharField(max_length=10)  # Ou utiliser un IntegerField
    directory = forms.CharField(max_length=250)
    role_id = forms.IntegerField()
