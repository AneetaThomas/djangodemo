from cart.models import Cart

def count_items(request):
    u=request.user
    count=0
    if request.user.is_authenticated:
        try:
            c=Cart.objects.filter(user=u)
            for i in c:
                count+=i.quantity
        except:
            count=0

    return {'c':count}

            