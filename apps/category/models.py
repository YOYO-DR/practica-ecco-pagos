from django.db import models

from config.settings import MEDIA_URL

# Create your models here.
class Category(models.Model):
    category_name=models.CharField(max_length=50,unique=True)
    description=models.CharField(max_length=255,blank=True)
    slug=models.CharField(max_length=100, unique=True)
    cat_image=models.ImageField(upload_to=f'{MEDIA_URL}photos/categories',blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name
    
