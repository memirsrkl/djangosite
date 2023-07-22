from django import forms
from .models import Ihas

class IhasForm(forms.ModelForm):
    class Meta:
        model = Ihas
        fields = '__all__'