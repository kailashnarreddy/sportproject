from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import *
from .models import *
from django.http import HttpResponse,Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from datetime import datetime


def isgen(request):

    if request.user.email=="sportsec@iitg.ac.in":
        return True
    else :
        return False    


def issup(request):
    if request.user.email=="chrsports@iitg.ac.in":     # mail id of Superindent
        return True
    else :
        return False      

def allclubs() :
    clubs_list=clubs.objects.all()                                                         # all clublists
    return clubs_list
    
# Create your views here.
def Home1(request):
    return render(request,'sportapp/home1.html')

@login_required(redirect_field_name='')      
def Index(request):                                                                       # home page view
    clubs_list=clubs.objects.all()
    secy=0                                                                 # to separate general users from secy
    superin=issup(request)
    gensec=isgen(request)
    rem_clubs=[]
                                                                   # to separate general users from secy
   
    if(clubs.objects.filter(email=request.user.email)):                      #to find if user is secy of any club or general user
                clubs_list=clubs.objects.filter(email=request.user.email)
                rem_clubs=clubs.objects.exclude(email=request.user.email)      
                secy=1 
                


                
    elif(gensec or superin):
           secy=1
    
    
    context = {
            'clubs_list':clubs_list,
            'super':superin,
                 'gensec':gensec,
                 'isre':secy,
                  'rem':rem_clubs
                    }            
    return render(request,'sportapp/home.html',context)

    
@login_required(redirect_field_name='')    
def ClubsView(request):                                                                    # club adding view
  if isgen(request) or issup(request)  :                                                   # only visible to gensec and superindent
    if request.method == 'POST':
        
        form = ClubForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('clubsList')

    else:
        form = ClubForm()
        context = {
            'form':form,
        }
    return render(request, 'sportapp/add_club.html', context)   
  raise Http404("Page does not exist")   


@login_required(redirect_field_name='')                     
def UpdateClubsView(request,pk):                                                             #pk of the club             # editing club information  
 if isgen(request) or issup(request) :                       
    if request.method == 'POST':
        form1 = ClubForm(request.POST)
        if form1.is_valid():
            form=form1.save(commit=False)
            clubs.objects.filter(pk=pk).update(name=form.name,secy_name=form.secy_name,email=form.email,dept=form.dept,prog=form.prog)
            return redirect('clubsList')

    else:
        club=clubs.objects.get(pk=pk)
        dict={                                              # for showing the prensent club information in the html form before editing (Get method)
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
        

@login_required(redirect_field_name='')    
def ClubsListView(request): #   clubslist page view
 
  
  if isgen(request) or issup(request) :  
   
    gensec=0
    if isgen(request):
        gensec=1
    context={'clubs_list':allclubs(),'gensec':gensec,'super':issup(request)}
    return render(request,'sportapp/clubs_list.html',context)
  raise Http404("Page does not exist")
@login_required(redirect_field_name='')        
def EquipmentView(request,pk):                                                      # adding club equipments 
   if  issup(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.available_quantity=post.total_quantity        
            post.sport=clubs.objects.get(pk=pk)                                      # linking equipment to clubs table
            post.save()
            return redirect('equipmentsList',pk=pk)
    else:
            
        form = EquipmentForm()
        context = {
            'form':form,
        }
    return render(request, 'sportapp/add_equipment.html', context)    
   raise Http404("Page does not exist")   


@login_required(redirect_field_name='')          
def addgeneral(request):                                                                 #adding general equipments view
  if issup(request) :  
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


def alphabet(d):                                                           #function for sorting based on name of the equipments
    return d.name        
@login_required(redirect_field_name='') 


def EquipmentListView(request,pk):                                        #Equipment list view

    clubs_list=clubs.objects.all()
    club=clubs.objects.get(pk=pk)                                           # retrieving the required club
    equipments=club.equipment_set.all()                                     # all equipments of the required club
    equipments1=list(equipments)                                            # converting the equipments in the required club to list data type to sort them in alphabetical order
    equipments1.sort(key=alphabet)            
    superin=issup(request)
    gensec=isgen(request)
    isre=0        
    rem_clubs=[]     
       
    ownclub=0                                                              # to separate general users from secy
   
    if(clubs.objects.filter(email=request.user.email)):                      #to find if user is secy of any club or general user
                clubs_list=clubs.objects.filter(email=request.user.email)
                rem_clubs=clubs.objects.exclude(email=request.user.email)      
                 
                isre=1   
                if(clubs.objects.get(email=request.user.email).email==club.email):
                   ownclub=1           
    elif(gensec or superin):
           isre=1

  
             
      
    context = {
             'clubs_list': clubs_list,
             'pk': pk,
            'equipments':equipments1,
            'super':superin,
            'gensec':gensec,
            'isre':isre,
            'rem':rem_clubs,
            
            'ownclub':ownclub
        }  
    
    return render(request, 'sportapp/equipments_list.html', context)   

@login_required(redirect_field_name='')    
def general(request):                #General equipment list view
 
    clubs_list=clubs.objects.all()
    equipments=generalequipment.objects.all()
    equipments1=list(equipments)       

    equipments1.sort(key=alphabet)
    superin=issup(request)
    gensec=isgen(request)
    isre=0
    rem_clubs=[]     
      
    if(clubs.objects.filter(email=request.user.email)):
                clubs_list=clubs.objects.filter(email=request.user.email)
                rem_clubs=clubs.objects.exclude(email=request.user.email)      
                 
                isre=1  
    elif(gensec or superin):
           isre=1  
        
    context = {
             'clubs_list': clubs_list,
            'equipments':equipments1,
            'super':superin,'gensec':gensec,
            'isre':isre,
            'rem':rem_clubs
         
        }  
  
    return render(request, 'sportapp/general.html', context)  


@login_required(redirect_field_name='')    
def deleteEquipmentView(request,id,pk):         #deleting equipments of club  
 if  issup(request)  : 
    if isgen(request) or issup(request) :
     a=equipment.objects.filter(id=id)              # id of the equipment
     a.delete()
     return redirect('equipmentsList',pk=pk)        # pk of the club
 else :
    raise Http404("Page does not exist")  


@login_required(redirect_field_name='')    
def generaldelete(request,id):                     # deleting general equipments
  if  issup(request):  
    a=generalequipment.objects.get(pk=id)
    a.delete()
    return redirect('general')                    # redirecting to general equipments list
  else :
    raise Http404("Page does not exist")


@login_required(redirect_field_name='')        
def IssueFormView(request,pk,id):                # issuing club equipments
   if  isgen(request) or clubs.objects.filter(email=request.user.email) : 
    equip=get_object_or_404(equipment, id=id)        # id of the equipment to te issued
   
    if request.method == 'POST':

        form = IssueForm(request.POST)
        if form.is_valid():
         post = form.save(commit=False)       
         post.equipment_name= equip                # linking equipment to the issue
         post.remark=None
         if isgen(request) :
             post.is_gen=1                         # if issued by general secy
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
            'maximum_value':equip.available_quantity                  # maximum quantity can be issued passed to html
        }
        return render(request, 'sportapp/Issue.html', context)  


   raise Http404("Page does not exist")
@login_required(redirect_field_name='')    
def generalissue(request,pk):                           # issuing general equipments
  if not issup(request) and (clubs.objects.filter(email=request.user.email) or isgen(request)) : 
    equip=get_object_or_404(generalequipment, pk=pk)
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  
            post.general_equipname=equip
            post.remark=None
            
            if isgen(request):
                post.is_gen=1;
            else :
                post.is_gen=0;
                post.user=clubs.objects.get(email=request.user.email)
            post.save()
            return redirect('generalIssueList')  
    else:
        form = IssueForm()
        context = {
            'form':form,
            'maximum_value':equip.available_quantity
        }
    return render(request, 'sportapp/Issue.html', {'form':form,'maximum_value':equip.available_quantity})      
  raise Http404("Page does not exist")

def myfuc(d):         #function to sort issues based on date
    return d.date

@login_required(redirect_field_name='')        
def IssueListView(request,pk):     # list of issues of club equipments by gen sec and club secy  and general equipment issues by club secy
   if request.user.email == clubs.objects.get(pk=pk).email or isgen(request) or issup(request):
    clubs_list=clubs.objects.all()
    club=clubs.objects.get(pk=pk)          
    equipments=club.equipment_set.all()
    
    tot_list=issue.objects.all()
    issue_list=[]
    secy=clubs.objects.get(pk=pk).email    # get the secy of the required club
    genlist=set()
    rem_clubs=[]     
       

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
    
    gensec=isgen(request)
    superin=issup(request)  
    context = {
             'clubs_list': clubs_list,
             'pk': pk,
            'issue_list':issue_list,
            'equipments':equipments,
            'gensec':gensec,
            'super':superin,
            'rem':rem_clubs,
        
        }     
    if gensec or superin :          
      return render(request, 'sportapp/Issue_list.html', context)
    else :
        clubs_list=clubs.objects.filter(email=request.user.email)
        context['rem']=clubs.objects.exclude(email=request.user.email)
        context['clubs_list']=clubs_list
        return render(request, 'sportapp/Issue_list.html', context)
   else:
       raise Http404("Page does not exist")


@login_required(redirect_field_name='')    
def generallist(request):                # issues of general equipments
   if  isgen(request) or issup(request) or clubs.objects.filter(email=request.user.email): 
    clubs_list=clubs.objects.all() 
    issue_list=issue.objects.filter(equipment_name=None)
    rem_clubs=[]
    iss=[]
    for i in range(len(issue_list)):               
                iss.append(issue_list[i])
    iss.reverse()            
    gensec=isgen(request)
    superin=issup(request)
    context={'issue_list':iss,'clubs_list':clubs_list,'gensec':gensec,'super':superin,'rem':rem_clubs}
    if gensec or issup(request) :          
     return render(request, 'sportapp/Issue_list.html', context)
    else :
        clubs_list=clubs.objects.filter(email=request.user.email)
        context['clubs_list']=clubs_list
        context['rem']=clubs.objects.exclude(email=request.user.email)
        return render(request, 'sportapp/Issue_list.html', context)    
   else :
    raise Http404("Page does not exist")

@login_required(redirect_field_name='')        
def gensecissuelist(request):          # all issues by general secretary
   if isgen(request):
       issue_list=issue.objects.filter(is_gen=1) 
       iss=[]
       for i in range(len(issue_list)):         
                iss.append(issue_list[i])       
       iss.reverse()
       context={'issue_list':iss,'clubs_list':allclubs(),'gensec':1,'super':issup(request)}
       return render(request,'sportapp/Issue_list.html',context)  
   raise Http404("Pasge does not exist")    


@login_required(redirect_field_name='')       
def returnequipment(request,pk,id):         # returning equipments of club
   if not issup(request):  
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
   raise Http404("Page does not exist")


@login_required(redirect_field_name='')       
def generalreturn(request,id):           #returning general equipments
   if not issup(request):  
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
   raise Http404("Page does not exist")     




@login_required(redirect_field_name='')    
def superindent(request,num):            # issue and return requests to superindent
   
    if issup(request):
        iss=issue.objects.filter(is_pending=True)
        context={'iss':iss}
        print(iss)
        suplist=[]
        for i in range(len(iss)):           
            suplist.append(iss[i])
        suplist.reverse()
        context={'iss':suplist,'clubs_list':allclubs(),'id':num}

        return render(request,'sportapp/superindent.html',context)  
    else :        
     raise Http404("Page does not exist")


@login_required(redirect_field_name='')         
def accept(request,pk):             #accepting issue or return by superindent
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
    
          
         

    return redirect('superindent',0)
   
   else: 
     iss=issue.objects.get(pk=pk)   
     if not iss.is_return :
       if iss.equipment_name :  
        if  iss.equipment_name.available_quantity < iss.quantity :
            messages.error(request, "Requested quantity is more than available quantity")
            return redirect('superindent',iss.pk)
       else :
         if  iss.general_equipname.available_quantity < iss.quantity :
            messages.error(request, "Requested quantity is more than available quantity")
            return redirect('superindent',iss.pk)       
     form=remarkform(initial={'remark': "None" })
     return render(request,'sportapp/remarkform.html',{'form':form})  
  else :        
     raise Http404("Page does not exist")  

@login_required(redirect_field_name='')    

def deny(request,pk):          # denying issue or return requests by superindent
 if issup(request):     
  if request.method=='POST': 
    form=remarkform(request.POST)
    if form.is_valid:
        post=form.save(commit=False)
    issue.objects.filter(pk=pk).update(is_pending=False,date=datetime.now(),remark=post.remark)
    return redirect('superindent',0)
  else :
    form=remarkform(initial={'remark': "None" })
    return render(request,'sportapp/remarkform.html',{'form':form}) 
 else :        
     raise Http404("Page does not exist")         


@login_required(redirect_field_name='')  
def total_list(request):
    if  issup(request) :
        iss=issue.objects.filter(is_pending=0)
        iss=iss.reverse()
        context={'issue_list':iss,
                  'super':issup(request),
                   'gensec':isgen(request),
                    'clubs_list':allclubs()   }
        return render(request,'sportapp/Total_list.html',context)    
    else:
        raise Http404("Page does not exist") 


