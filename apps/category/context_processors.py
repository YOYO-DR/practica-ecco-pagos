# una funcion que retorna algo que pueda ser llamado por cada template, en este caso, las categorias y debo pasarlo en un diccionario y recibe un request
from .models import Category

def menu_links(request):
    links = Category.objects.all()
    return {'links':links}