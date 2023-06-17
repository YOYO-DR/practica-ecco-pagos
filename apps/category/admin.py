from django.contrib import admin
from .models import Category

class CategoryAadmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)} # para que el campo slug se genere automaticamente con lo que se escriba en category_name, asi, puedo utilizar el slug para el link de la categoria
    list_display = ('category_name','slug') # crear las columnas del category_name y slug 

admin.site.register(Category,CategoryAadmin)
