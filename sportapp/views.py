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
    user = request.user
    print(user)
    print(user.username)
    print(user.email)
    print(type(user))
    print(type(user.username))
    print(type(user.email))
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
    c=club.name
    context = {
             'clubs_list': clubs_list,
             'pk': pk,
            'equipments':equipments,
            'c':c,
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
            # if post.quantity > equip.available_quantity:
            #     return HttpResponse('Cannot be issued')
            # else:   
         quantity = equip.available_quantity-post.quantity
         post.equipment_name= equipment.objects.get(id=id)
               
         post.save()
            
         return redirect('IssueList',pk=pk)  

    else:
        equip=get_object_or_404(equipment, id=id)
        form = IssueForm()
        context = {
            'form':form,
            'maximum_value':equip.available_quantity
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
            if (str(o.equipment_name) == str(equip.name)):
                issue_list.append(o)
    issue_list.reverse()          
    context = {
             'clubs_list': clubs_list,
             'pk': pk,
            'issue_list':issue_list,
            'equipments':equipments,
        }
    return render(request, 'sportapp/Issue_list.html', context)
def returnequipment(request,pk,id):
    if request.method == 'POST':
        eq=get_object_or_404(equipment,pk=id)
        form = ReturnForm(request.POST)
        quan=request.POST.get('quantity')
        if form.is_valid():
            post = form.save(commit=False)
            iss=issue(name=post.name,equipment_name=eq,roll=post.roll,quantity=quan,is_return=True)
            iss.save()
            return redirect('IssueList',pk=pk)  

    else:
        form = ReturnForm()
        eq=get_object_or_404(equipment,pk=id)
        context = {
            'form':form,
            'maximum_value':eq.total_quantity-eq.available_quantity
        }
    return render(request, 'sportapp/return_form.html', context)    

def superindent(request):
    user = request.user
    if user.email=="n.kailash@iitg.ac.in":
        iss=issue.objects.filter(is_pending=True)
        print(iss)
        context={'iss':iss}
        return render(request,'sportapp/superindent.html',context)
    else:
        return redirect('Home')
def accept(request,pk):
    issue.objects.filter(pk=pk).update(is_pending=False,req=True)
    isl=issue.objects.get(pk=pk)
    ik=isl.equipment_name.id
    eq=equipment.objects.get(pk=ik)
    if isl.is_return==False:
        equipment.objects.filter(pk=ik).update(available_quantity=eq.available_quantity-isl.quantity)
    
    if isl.is_return==True:
        equipment.objects.filter(pk=ik).update(available_quantity=eq.available_quantity+isl.quantity)    

    return redirect('superindent')
def deny(request,pk):
     issue.objects.filter(pk=pk).update(is_pending=False)
    
     
     return redirect('superindent')

class TotalListView(ListView):
    model=issue
    template_name='sportapp/Total_list.html'













    








