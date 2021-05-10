from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import *
from .models import *
from django.http import HttpResponse,Http404



from datetime import datetime




def isgen(request):
    if request.user.email=="bkartheek@iitg.ac.in":
        return True
    else :
        return False    


def issup(request):
    if request.user.email=="n.kailash@iitg.ac.in":
        return True
    else :
        return False    

def allclubs() :
    clubs_list=clubs.objects.all()
    return clubs_list
    
# Create your views here.

def Index(request):
    clubs_list=clubs.objects.all()
  
    user=request.user
  
    if isgen(request) or issup(request):
             context = {
            'clubs_list':clubs_list,
            'super':issup(request),
                 'gensec':isgen(request),
                    }
             return render(request,'sportapp/home.html',context)
    else:
        
        clubs_list=clubs.objects.all()
        for club in clubs_list:
            if (str(club.email)==str(user.email)):
                 clu=[]
                 clu.append(club)
                 context = {
                 'clubs_list':clu,
                 'super':issup(request)
                  
                    }
                 return render(request,'sportapp/home.html',context)

       
    raise Http404("Page does not exist")


def ClubsView(request):
  if isgen(request) or issup(request)  :
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
  raise Http404("Page does not exist") 
def UpdateClubsView(request,pk):
 if isgen(request) or issup(request) :  
    if request.method == 'POST':
        form1 = ClubForm(request.POST)
        if form1.is_valid():
            form=form1.save(commit=False)
            clubs.objects.filter(pk=pk).update(name=form.name,secy_name=form.secy_name,email=form.email,dept=form.dept,prog=form.prog)
            return redirect('clubsList')

    else:
        club=clubs.objects.get(pk=pk)
        dict={
            "name":club.name,
            "secy_name":club.secy_name,
            "email":club.email,
            "dept":club.dept,
            "prog":club.prog
        }
        form = ClubForm(initial=dict)
        context = {
            'form':form,
        }
    return render(request, 'sportapp/add_club.html', context)   

 raise Http404("Page does not exist")  
        

def ClubsListView(request):
  if isgen(request) or issup(request) :  
   
    gensec=0
    if isgen(request):
        gensec=1
    context={'clubs_list':allclubs(),'gensec':gensec,'super':issup(request)}
    return render(request,'sportapp/clubs_list.html',context)
  raise Http404("Page does not exist")   
def EquipmentView(request,pk):
   if isgen(request) or issup(request):
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
   raise Http404("Page does not exist")      
def addgeneral(request):
  if issup(request) or isgen(request):  
    if request.method == 'POST':
        form = generalequipmentform(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.available_quantity=post.total_quantity
            post.save()
            return redirect('general')
    else:       
        form = generalequipmentform()
        context = {
            'form':form,
        }
    return render(request, 'sportapp/add_equipment.html', context) 
  raise Http404("Page does not exist")        
def alphabet(d):
    return d.name           
def EquipmentListView(request,pk):
   if request.user.email == clubs.objects.get(pk=pk).email or isgen(request) or issup(request):
    clubs_list=clubs.objects.all()
    club=clubs.objects.get(pk=pk)
    equipments=club.equipment_set.all()
    equipments1=list(equipments)

    equipments1.sort(key=alphabet)
    c=club.name
    superin=0
    gensec=0
    
    if issup(request)  :
      superin=1
    if isgen(request) :
      gensec=1 
    if superin or gensec :
     context = {
             'clubs_list': clubs_list,
             'pk': pk,
            'equipments':equipments1,
            'c':c,
            'super':superin,
            'gensec':gensec
        }
     return render(request, 'sportapp/equipments_list.html', context)     
    else :
       clubs_list=clubs.objects.filter(email=request.user.email)
       context = {
             'clubs_list': clubs_list,
             'pk': pk,
            'equipments':equipments,
            'c':c,
            'super':superin,
            'gensec':gensec
        }
       return render(request, 'sportapp/equipments_list.html', context)      
   else:
       raise Http404("Page does not exist")

def general(request):
    clubs_list=clubs.objects.all()
    equipments=generalequipment.objects.all()
    equipments1=list(equipments)

    equipments1.sort(key=alphabet)
    superin=0
    gensec=0
    
    if issup(request) :
      superin=1
    if isgen(request) :
      gensec=1 
    if gensec or superin :
      context = {
             'clubs_list': clubs_list,
            'equipments':equipments1,
            'super':superin,'gensec':gensec
        }
     
      return render(request,'sportapp/general.html',context)
    else :
       clubs_list=clubs.objects.filter(email=request.user.email)
       context = {
             'clubs_list': clubs_list,
            'equipments':equipments,
            'super':superin,'gensec':gensec
        }
     
       return render(request,'sportapp/general.html',context)


def deleteEquipmentView(request,id,pk):
 if isgen(request) or issup(request)  : 
    if isgen(request) or issup(request) :
     a=equipment.objects.filter(id=id)
     a.delete()
     return redirect('equipmentsList',pk=pk)
 else :
    raise Http404("Page does not exist")     

def generaldelete(request,id):
  if isgen(request) or issup(request):  
    a=generalequipment.objects.get(pk=id)
    a.delete()
    return redirect('general')
  else :
    raise Http404("Page does not exist")
def IssueFormView(request,pk,id):
    equip=get_object_or_404(equipment, id=id)
   
    if request.method == 'POST':

        form = IssueForm(request.POST)
        if form.is_valid():
         post = form.save(commit=False)
            
         quantity = equip.available_quantity-post.quantity
         post.equipment_name= equip
         post.remark=None
         if isgen(request) :
             post.is_gen=1
         else :
             post.is_gen=0
             post.user=equip.sport

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


def generalissue(request,pk):
    equip=get_object_or_404(generalequipment, pk=pk)
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  
            quantity = equip.available_quantity-post.quantity
            post.general_equipname=equip
            post.remark=None
            
            if isgen(request):
                post.is_gen=1;
            else :
                post.is_gen=0;
                post.user=clubs.objects.get(email=request.user.email)
            post.save()
            return redirect('general')  
    else:
        form = IssueForm()
        context = {
            'form':form,
            'maximum_value':equip.available_quantity
        }
    return render(request, 'sportapp/Issue.html', {'form':form,'maximum_value':equip.available_quantity})      


def myfuc(d):  
    return d.date
def IssueListView(request,pk):
   if request.user.email == clubs.objects.get(pk=pk).email or isgen(request) or issup(request):
    clubs_list=clubs.objects.all()
    club=clubs.objects.get(pk=pk)
    equipments=club.equipment_set.all()
    
    tot_list=issue.objects.all()
    issue_list=[]
    secy=clubs.objects.get(pk=pk).email 
    genlist=set()
    
    for equip in equipments:
        for o in tot_list:
           if o.equipment_name : 
            if str(o.equipment_name.name) == str(equip.name):
              
              issue_list.append(o)
           elif  o.user:
            
            if   o not in genlist:
             if str(o.user.email) == str(secy):
              
               
                issue_list.append(o)
                genlist.add(o)

    issue_list.reverse()  
    issue_list.sort(reverse=True,key=myfuc)
    
    gensec=0
    if isgen(request):
        gensec=1    
    if gensec or issup(request) :          
     context = {
             'clubs_list': clubs_list,
             'pk': pk,
            'issue_list':issue_list,
            'equipments':equipments,
            'gensec':gensec,
            'super':issup(request)
        }
     return render(request, 'sportapp/Issue_list.html', context)
    else :
        clubs_list=clubs.objects.filter(email=request.user.email)
        context = {
             'clubs_list': clubs_list,
             'pk': pk,
            'issue_list':issue_list,
            'equipments':equipments,
            'gensec':gensec,
            'super':issup(request)
        }
        return render(request, 'sportapp/Issue_list.html', context)
   else:
       raise Http404("Page does not exist")

def generallist(request):
    clubs_list=clubs.objects.all() 
    issue_list=issue.objects.filter(equipment_name=None)
    
    iss=[]
    for i in range(len(issue_list)):               
                iss.append(issue_list[i])
    iss.reverse()            
    gensec=0
    if isgen(request):
        gensec=1
    if gensec or issup(request) :          
     context={'issue_list':iss,'clubs_list':clubs_list,'gensec':gensec,'super':issup(request)}
     return render(request, 'sportapp/Issue_list.html', context)
    else :
        clubs_list=clubs.objects.filter(email=request.user.email)
        context={'issue_list':iss,'clubs_list':clubs_list,'gensec':gensec,'super':issup(request)}
        return render(request, 'sportapp/Issue_list.html', context)    

    
def gensecissuelist(request):
   if isgen(request):
       issue_list=issue.objects.filter(is_gen=1) 
       iss=[]
       for i in range(len(issue_list)):         
                iss.append(issue_list[i])       
       iss.reverse()
       context={'issue_list':iss,'clubs_list':allclubs(),'gensec':1,'super':issup(request)}
       return render(request,'sportapp/Issue_list.html',context)  
   raise Http404("Pasge does not exist")    
def returnequipment(request,pk,id):
    if request.method == 'POST':
        eq=get_object_or_404(equipment,pk=id)
        form = ReturnForm(request.POST)
        quan=request.POST.get('quantity')
        if form.is_valid():
            post = form.save(commit=False)
            post.remark=None
            post.equipment_name=eq
            post.is_return = True
            if isgen(request) :
             post.is_gen=1
            else :
             post.is_gen=0
             post.user=eq.sport

            post.save()
        
            return redirect('IssueList',pk=pk)  
    else:
        form = ReturnForm()
        eq=get_object_or_404(equipment,pk=id)
        context = {
            'form':form,
            'maximum_value':eq.total_quantity-eq.available_quantity
        }
        return render(request, 'sportapp/return_form.html', context)    

def generalreturn(request,id):
    if request.method == 'POST':
        eq=get_object_or_404(generalequipment,pk=id)
        form = ReturnForm(request.POST)
        quan=request.POST.get('quantity')
        if form.is_valid():
            post = form.save(commit=False)
            post.remark=None
            post.is_return= True
            post.general_equipname = eq
            if isgen(request):
                post.is_gen=1;
            else :
                post.is_gen=0;
                post.user=clubs.objects.get(email=request.user.email)
            post.save()
            return redirect('generalIssueList')
    else:
        form = ReturnForm()
        eq=get_object_or_404(generalequipment,pk=id)
        context = {
            'form':form,
            'maximum_value':eq.total_quantity-eq.available_quantity
        }
        return render(request, 'sportapp/return_form.html', context)
        





def superindent(request):
   
    if issup(request):
        iss=issue.objects.filter(is_pending=True)
        context={'iss':iss}
        print(iss)
        suplist=[]
        for i in range(len(iss)):           
            suplist.append(iss[i])
        suplist.reverse()
        context={'iss':suplist,'clubs_list':allclubs()}
        

        return render(request,'sportapp/superindent.html',context)  
    else :        
     raise Http404("Page does not exist")
def accept(request,pk):
  if issup(request):   
   if request.method=='POST': 
    form=remarkform(request.POST)
    if form.is_valid:
        post=form.save(commit=False)
    issue.objects.filter(pk=pk).update(is_pending=False,req=True,date=datetime.now(),remark=post.remark)
    isl=issue.objects.get(pk=pk)
    
    
    if isl.equipment_name:
       ik=isl.equipment_name.id
       eq=equipment.objects.get(pk=ik)
       if isl.is_return==False:
        equipment.objects.filter(pk=ik).update(available_quantity=eq.available_quantity-isl.quantity)
        
       if isl.is_return==True:
        equipment.objects.filter(pk=ik).update(available_quantity=eq.available_quantity+isl.quantity)
    else :
       ik=isl.general_equipname.id 
       eq=generalequipment.objects.get(pk=ik)  
       if isl.is_return==False:
        generalequipment.objects.filter(pk=ik).update(available_quantity=eq.available_quantity-isl.quantity)
        
       if isl.is_return==True:
        generalequipment.objects.filter(pk=ik).update(available_quantity=eq.available_quantity+isl.quantity)
    
          
         

    return redirect('superindent')
   
   else: 
     form=remarkform(initial={'remark': "None" })
     return render(request,'sportapp/remarkform.html',{'form':form})  
  else :        
     raise Http404("Page does not exist")  

def deny(request,pk):
 if issup(request):     
  if request.method=='POST': 
    form=remarkform(request.POST)
    if form.is_valid:
        post=form.save(commit=False)
    issue.objects.filter(pk=pk).update(is_pending=False,date=datetime.now(),remark=post.remark)
    return redirect('superindent')
  else :
    form=remarkform()
    return render(request,'sportapp/remarkform.html',{'form':form}) 
 else :        
     raise Http404("Page does not exist")          

class TotalListView(ListView):
    model=issue
    template_name='sportapp/Total_list.html'


