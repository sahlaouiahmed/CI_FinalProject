from django.urls import path
from . import views
from .views import product_list, product_detail, add_to_cart, cart_view, update_cart, delete_cart_item,checkout,payment_success,payment_cancel


urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'), 
    path('cart/', cart_view, name='cart_view'),
    path('update-cart/<int:item_id>/', update_cart, name='update_cart'), 
    path('delete-cart-item/<int:item_id>/', delete_cart_item, name='delete_cart_item'),
    path('checkout/', checkout, name='checkout'),
    
    path('success/',payment_success, name='payment_success'),
    path('cancel/',payment_cancel, name='payment_cancel'),

]
