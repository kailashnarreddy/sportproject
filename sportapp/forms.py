from .models import *
from django import forms


class ClubForm(forms.ModelForm):
    class Meta:
        model=clubs
        fields = '__all__'
        

class EquipmentForm(forms.ModelForm):
    class Meta:
        model=equipment
        fields=['name','total_quantity','specification']

class IssueForm(forms.ModelForm):
    class Meta:
        model=issue
        fields=['roll','name','quantity']
class ReturnForm(forms.ModelForm):
    class Meta:
        model=issue
        fields=['roll','name','quantity']