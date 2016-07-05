from django import forms
from tables.choices import RIPENESS_CHOICES

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()