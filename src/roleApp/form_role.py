from django import forms


class RoleForm(forms.Form):
    name = forms.CharField(max_length=100)
    permissions = forms.CharField()