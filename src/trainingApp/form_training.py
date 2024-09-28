from django import forms

class TrainingForm(forms.Form):
    name = forms.CharField(max_length=250)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    startDate = forms.DateField()
    endDate = forms.DateField()
    type = forms.CharField(max_length=50, required=False)
    directory = forms.CharField(max_length=250)
    fieldId = forms.IntegerField()
    structureId = forms.IntegerField()
