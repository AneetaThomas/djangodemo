from django.shortcuts import render,redirect
from shop.models import product
from cart.models import Cart,Order_details,Payment
from django.contrib.auth.decorators import login_required
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login
# Create your views here.
@login_required
def addtocart(request,i):
    p=product.objects.get(id=i)
    u=request.user    # assgin the detals of the corresponding user

    try:
        c=Cart.objects.get(product=p,user=u)   #if a particular user for the particular pdt exist
        if p.stock>0:
            c.quantity+=1
            c.save()
            p.stock-=1
            p.save()
    except:
        if p.stock>0:           #if a particular pdt doesn't exist
            c=Cart.objects.create(product=p,user=u,quantity=1)
            c.save()
            p.stock-=1
            p.save()
    return redirect('cart:cartview')

def cartview(request):         # to check out

    u=request.user   
    try:
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total+=i.quantity*i.product.price
    except:
        pass
    context={'cart':c,'total':total}
    return render(request,'cart.html',context)

def cartremove(request,i):
    p=product.objects.get(id=i)
    u=request.user    # assgin the detals of the corresponding user

    try:
        c=Cart.objects.get(product=p,user=u)
        if c.quantity>1:
            c.quantity-=1
            c.save()
            p.stock+=1
            p.save()
        else:
            c.delete()
            p.stock +=1
            p.save()
    except:
        pass
    
    return redirect('cart:cartview')

def cartdelete(request,i):
    p=product.objects.get(id=i)
    u=request.user 
    c=Cart.objects.get(product=p,user=u)
    c.delete()
    p.stock +=c.quantity    #if there is two or more product is available 
    p.save()
    return redirect('cart:cartview')

def placeorder(request):

    if(request.method=="POST"):
        address=request.POST['adrs']
        phone=request.POST['phno']
        pin=request.POST['pin']

        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total+=i.quantity*i.product.price
        
        total1=int(total*100)
        print("total",total)
        print("total1",total1)
        
        client=razorpay.Client(auth=('rzp_test_6wXKKD3es3TM9F','DXhOQeFdZ0JXqqRiV5ggOCh1'))
    # creates client connection using razorpay is and secrect code
        response_payment=client.order.create(dict(amount=total1,currency="INR"))
        # creates an order with razorpay using razorpay client
        print(response_payment)

        order_id=response_payment['id']
        status=response_payment['status']

        if(status=="created"):
            p=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            p.save()

            for i in c:
                o=Order_details.objects.create(pro=i.product,usr=u,no_of_items=i.quantity,address=address,phone_no=phone,pin=pin,order_id=order_id)
                o.save()

        response_payment["name"]=u.username        

        context={'payment':response_payment}
        return render(request,"payment.html",context)

    return render(request,"order.html")

@csrf_exempt
def Payment_status(request,u):
    usr=User.objects.get(username=u)
    if not request.user.is_authenticated:
        login(request,usr)

    if(request.method=="POST"):
        response=request.POST
        print(response)

        param_dict={
            'razorpay_order_id':response['razorpay_order_id'],
            'razorpay_payment_id':response['razorpay_payment_id'],
            'razorpay_signature':response['razorpay_signature']
        }
        # To check the validity of razorpay signanture 
        client=razorpay.Client(auth=('rzp_test_6wXKKD3es3TM9F','DXhOQeFdZ0JXqqRiV5ggOCh1'))  #to create razorpay client
        print(client)
        status=client.utility.verify_payment_signature(param_dict) # to check the authenticity of razorpay signature
        print(status)

      # to retrive a particular record from payment table matching with razorpay response orderid 
        p=Payment.objects.get(order_id=response['razorpay_order_id'])
        p.razorpay_payment_id=response['razorpay_payment_id']
        p.paid=True
        p.save()

        # to retrive records from order_details table matching with razorpay response order id
        o=Order_details.objects.filter(order_id=response['razorpay_order_id'])
        for i in o:
            i.payment_status="completed"
            i.save()    # check in admin table were data is saved

            # to delete items from cart
            
            c=Cart.objects.filter(user=usr)
            c.delete()



    return render(request,'payment_status.html',context={'status':status})


@login_required
def orderview(request):
    u=request.user
    o=Order_details.objects.filter(usr=u)
    print(o)
    context={'orders':o}
    return render(request,'orderview.html',context)



    











 