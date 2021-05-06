from .models import *
from django import forms

departments=[('CSE','CSE'),('MNC','MNC'),('EEE','EEE'),('ECE','ECE'),('CL','CL'),('CST','CST'),('EP','EP'),('BT','BT'),('MECH','MECH'),('CIVIL','CIVIL'),('others','others')]
programs=[('BTECH','BTECH'),('MTECH','MTECH'),('B.DES','B.DES'),('M.DES','M.DES'),('PhD','PhD'),('M.S.(R)','M.S.(R)'),('M.A.','M.A.'),('M.Sc.','M.Sc.'),('others','others')]
class ClubForm(forms.ModelForm):
    dept=forms.CharField(widget=forms.Select(choices=departments))
    prog=forms.CharField(widget=forms.Select(choices=programs))
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
        fields=['roll','name','quantity','remark']
class ReturnForm(forms.ModelForm):
    class Meta:
        model=issue
        fields=['roll','name','quantity','remark']
class generalequipmentform(forms.ModelForm):
    class Meta:
        model=generalequipment
        fields=['name','total_quantity','specification']

        
