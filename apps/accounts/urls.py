from django.urls import path
from .views import *

urlpatterns = [
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('dashboard/',dashboard,name='dashboard'),
    path('',dashboard,name='dashboard'),
    path('forgotPassword/',forgotPassword,name='forgotPassword'),
    path('resetPassword_validate/<uidb64>/<token>/',resetPassword_validate,name='resetPassword_validate'),
    path('resetPassword/',resetPassword,name='resetPassword'),
    path('activate/<uidb64>/<token>/',activate,name='activate'),
    path('my_orders/',my_orders,name='my_orders'),
    path('edit_profile/',edit_profile,name='edit_profile'),
]

