from django.shortcuts import render,redirect
from shop.models import category,product
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def categories(request):
    c=category.objects.all()   # here a category model is created
    context={'cat':c}          # 
    return render(request,"categories.html",context)

@login_required
def products(request,p):     # here p receives the category id (1 usage -1 dy namic)
    c=category.objects.get(id=p)   # reads a particular category object using id
    k=product.objects.filter(category=c)  # reads all products under a particular category object -foreign key
    context={'cat':c,'pro':k}      # context={'cat':c} is given to diplay image from category page 
                                   #send data from view function to html page 
    return render(request,"products.html",context)
@login_required    
def productdetails(request,p):
    d=product.objects.get(id=p)  #reads data of a particular id
    context={'detl':d}             #used to send data from view function to html page
    return render(request,"details.html",context)

def register(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        cp=request.POST['cp']
        f=request.POST['f']
        l=request.POST['l']
        e=request.POST['e']

        if(p==cp):
            x=User.objects.create_user(username=u,password=p,email=e,first_name=f,last_name=l)
            x.save()
            return redirect ('shop:categories')
        else:
            return HttpResponse('Passwords are not valid')
    return render(request,'register.html')


def user_login(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        user=authenticate(username=u,password=p)

        if user: #if matching user exist
            login(request,user)
            return redirect ('shop:categories')
        else: #if no matching user
            return HttpResponse ("invalid Credentials")
    return render(request,"login.html")
@login_required
def user_logout(request):
    logout(request)
    return redirect('shop:login')

def addcat(request):
    if(request.method=='POST'):
        n=request.POST['n']
        i=request.FILES.get('i')
        d=request.POST['d']

        c=category.objects.create(name=n,image=i,description=d)
        c.save()
        return redirect('shop:categories')
    return render(request,"addcat.html")

def addpro(request):

    if(request.method=='POST'):
        n=request.POST['n']
        i=request.FILES.get('i')
        d=request.POST['d']
        s=request.POST['s']
        p=request.POST['p']
        c=request.POST['c']

        cat=category.objects.get(name=c)

        p=product.objects.create(name=n,image=i,desc=d,stock=s,price=p,category=cat)
        p.save()

        return redirect('shop:categories')


    return render(request,"addpro.html")

def addstock(request,p):
    pdt=product.objects.get(id=p)
    
    if(request.method=='POST'):
        pdt.stock=request.POST['n']
        pdt.save()
        return redirect('shop:productdetails',p)
    context={'pro':pdt}
    return render(request,addstock.html,context)
    