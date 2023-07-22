from django import forms
from .models import admins

class adminslogin(forms.ModelForm):
    class Meta:
        model = admins
        fields = '__all__'