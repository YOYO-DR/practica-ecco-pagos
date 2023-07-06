from django.urls import path
from .views import StoreView,ProductDetailView,SearchView, submit_review
urlpatterns = [
    path('',StoreView.as_view(),name="store"),
    path('category/<slug:category_slug>/',StoreView.as_view(),name="products_by_category"),
    path('category/<slug:category_slug>/<slug:product_slug>/',ProductDetailView.as_view(),name="product_detail"),
    path('search/',SearchView.as_view(),name="search"),
    path('submit_review/<int:product_id>/',submit_review,name="submit_review")
]
