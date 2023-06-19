from django.db import models
from django.urls import reverse
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

    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])

    def __str__(self):
        return self.product_name

# para las funciones para retornarlos valores segun el filtro que se haga
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)
    
    def tallas(self):
        return super(VariationManager,self).filter(variation_category='talla',is_active=True)

variation_category_choice = (
    ('color','color'),
    ('talla','talla')
)

# para guardar las variantes de los productos
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # los diferentes valores de los productos
    variation_category=models.CharField(max_length=100,choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)

    # relaciono el modelo con el manager para que los modelos puedan accedes a las 2 funciones
    objects=VariationManager()

    def __str__(self):
        return self.product.product_name

