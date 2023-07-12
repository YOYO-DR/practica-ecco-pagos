from django.contrib import admin
from .models import Product, ReviewRating,Variation,ProductGallery
import admin_thumbnails # django-admin-thumbnails


#para mostrarlo en el admin de producto, un preview
#con este decorador le digo que haga el preview del campo image de ese modelo
@admin_thumbnails.thumbnail('image')
class ProductGaleryInline(admin.TabularInline):
    model = ProductGallery
    extra=1

class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','price','stock','category','modified_date','is_available')
    prepopulated_fields={'slug':('product_name',)}
    inlines=[ProductGaleryInline] # le agrego para que aparezaca abajo del admin y tambien se va a poder guardar desde ahi

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
admin.site.register(ProductGallery)