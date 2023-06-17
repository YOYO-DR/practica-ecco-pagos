from django.db import models
from apps.category.models import Category

from config.settings import MEDIA_URL

# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=200, unique=True)
    slug=models.CharField(max_length=200, unique=True)
    description=models.TextField(max_length=500, blank=True)
    price=models.IntegerField()
    images = models.ImageField(upload_to=f"{MEDIA_URL}/photos/products")
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    


