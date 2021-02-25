from django.urls import path,include
from . views import store,cart,checkout,updateitem,processorder,home

urlpatterns = [
    path('', store, name="store"),
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('update_item/',updateitem, name="updateitem"),
    path('process_order/',processorder,name="processorder"),
    path('home/',  home, name="home")

]
