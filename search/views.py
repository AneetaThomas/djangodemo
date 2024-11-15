from django.shortcuts import render
from shop.models import product
from django.db.models import Q
# Create your views here.
def search_function(request):
    if(request.method=='POST'):
        query=request.POST['q'] #reads the query value
        print(query)
        p=product.objects.filter(Q(name__icontains=query) | Q(desc__icontains=query) ) #filter the records matching with the query
        context={'pro':p,'query':query}

       
    return render(request,'search.html',context)