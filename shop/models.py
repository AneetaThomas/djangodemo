from django.db import models

# Create your models here.
class category(models.Model):
    name=models.CharField(max_length=30)
    description=models.TextField()
    image=models.ImageField()

    def __str__(self):
        return self.name
    
class product(models.Model):
    name=models.CharField(max_length=20)
    desc=models.TextField()
    image=models.ImageField(upload_to="products")
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True) #one time
    updated=models.DateTimeField(auto_now=True) #change every time we update record
    category=models.ForeignKey(category,on_delete=models.CASCADE)

    def __str__(self):
        return self.name