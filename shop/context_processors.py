from shop.models import category

def menu_links(request):
    c=category.objects.all()
    return {'links':c}