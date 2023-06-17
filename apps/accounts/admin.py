from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

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

admin.site.register(Account,AccountAdmin) # se lo paso como segundo parametro