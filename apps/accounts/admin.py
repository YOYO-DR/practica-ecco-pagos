from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
from django.utils.html import format_html

class AccountAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','username','last_login','date_joined','is_active') # para que aparezca como unas columnas en la parte del account 

    list_display_links = ('email','first_name','last_name') # esto es para que esas columnas se vuelvan links hacia la modificacion de ese usuario
    readonly_fields = ('last_login','date_joined') # para que estos datos sean de solo lectura
    ordering=('-date_joined',) #para ordenar por el date_joined
    # como es tupla debo ponerle esa ","
        
    # solo inicializo esto
    filter_horizontal=()
    list_filter=()
    fieldsets=()

class UserProfileAdmin(admin.ModelAdmin):
    #creo una funcion para mostrar la imagen de perfil del usuario
    #el object hacer referencia a UserProfile que es el modelo en el cual se esta personalizando
    def thumbail(self,object):
        #utilizo el format_html para retornar un html a mostrar en el admin
        return format_html('<img src="{}" width="30 style="border-radius:50%;"'.format(object.profile_picture.url) )
    # le agrego la propiedad shor_description a la funcion creada la cual sera el titulo de ese campo
    thumbail.short_description = 'Imagen de perfil'
    #y aqui pongo el nombre de la funcion junto los atributos que quiero que vea
    list_display=('thumbail','user','city','state','country')

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Account,AccountAdmin) # se lo paso como segundo parametro