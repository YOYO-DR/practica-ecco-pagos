from django.contrib import admin
from .models import Product, ReviewRating,Variation

class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','price','stock','category','modified_date','is_available')
    prepopulated_fields={'slug':('product_name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display=('product','variation_category','variation_value','is_active')

    # para decirle que valores se pueden editar en la previsualización
    list_editable = ('is_active',)

    #para agregar un filtro segun estos datos
    list_filter=('product','variation_category','variation_value','is_active')

# primer valor el modelo y luego el modelo de administración
admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(ReviewRating)