from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import *
from .models import *
from django.http import HttpResponse


# Create your views here.


def Index(request):
    clubs_list=clubs.objects.all()
    context = {
            'clubs_list':clubs_list,
        }
    return render(request,'sportapp/home.html',context)
    


def ClubsView(request):
    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request,f'Your club has been saved!')
            return redirect('clubsList')

    else:

        form = ClubForm()
        context = {
            'form':form,
        }
    return render(request, 'sportapp/add_club.html', context)   

class UpdateClubView(UpdateView):
    model = clubs
    fields = ['name','secy_name','email']
    template_name = 'sportapp/add_club.html'    

class ClubsListView(ListView):
    model = clubs
    template_name = 'sportapp/clubs_list.html'

def EquipmentView(request,pk):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.available_quantity=post.total_quantity
            post.sport=clubs.objects.get(pk=pk)
            post.save()
            messages.success(request,f'Your Equipment has been saved!')
            return redirect('equipmentsList',pk=pk)
    else:
            
        form = EquipmentForm()
        context = {
            'form':form,
        }
    return render(request, 'sportapp/add_equipment.html', context)       
        
           
def EquipmentListView(request,pk):
    clubs_list=clubs.objects.all()
    club=clubs.objects.get(pk=pk)
    equipments=club.equipment_set.all()
    context = {
             'clubs_list': clubs_list,
             'pk': pk,
            'equipments':equipments,
        }
    return render(request, 'sportapp/equipments_list.html', context)      



def deleteEquipmentView(request,id,pk):
    a=equipment.objects.filter(id=id)
    a.delete()
    return redirect('equipmentsList',pk=pk)


def IssueFormView(request,pk,id):
    equip=get_object_or_404(equipment, id=id)
    if request.method == 'POST':

        form = IssueForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if post.quantity > equip.available_quantity:
                return HttpResponse('Cannot be issued')
            else:   
                quantity = equip.available_quantity-post.quantity
                post.equipment_name= equipment.objects.get(id=id)
                equipment.objects.filter(id=id).update(available_quantity=quantity)
                post.save()
            return redirect('IssueList',pk=pk)  

    else:
        form = IssueForm()
        context = {
            'form':form,
        }
    return render(request, 'sportapp/Issue.html', context)      



def IssueListView(request,pk):
    clubs_list=clubs.objects.all()
    club=clubs.objects.get(pk=pk)
    equipments=club.equipment_set.all()
    tot_list=issue.objects.all()
    issue_list=[]
    for equip in equipments:
        for o in tot_list:
            if (o.equipment_name == equip.name):
                issue_list.append(obj)
       
    context = {
             'clubs_list': clubs_list,
             'pk': pk,
            'issue_list':issue_list,
            'equipments':equipments,
        }
    return render(request, 'sportapp/Issue_list.html', context)     




class TotalListView(ListView):
    model=issue
    template_name='sportapp/Total_list.html'













    








