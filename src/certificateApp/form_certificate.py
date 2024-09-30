from django import forms

class CertificateForm(forms.Form):
    title = forms.CharField(max_length=250)
    description = forms.CharField(widget=forms.Textarea)
    date = forms.DateField()
    status = forms.CharField(max_length=50)
    type = forms.CharField(max_length=50, required=False)
    level = forms.CharField(max_length=50, required=False)
    studentId = forms.IntegerField()
