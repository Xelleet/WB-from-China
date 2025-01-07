from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('wb_admin/', views.wb_admin, name='wb_admin'),
    path('product/<int:index>', views.product, name='product'),
    path('add_admin/', views.add_admin, name='add_admin'),
    #path('login_admin/', views.login_admin, name='login_admin'),
    path('delete_product/', views.delete_product, name='delete_product'),
    path('add_to_cart/<int:index>', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:index>', views.remove_from_cart, name='remove_from_cart'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout')
]#