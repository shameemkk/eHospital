from django import forms
from . models import Patient
class UserCreationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'