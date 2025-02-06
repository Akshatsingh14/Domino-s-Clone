from django.urls import path
from . import views

urlpatterns = [
    path('home', views.index, name = 'index'),
    path('signup', views.register, name = 'register'),
    path('', views.log_in, name = 'log_in'),
    path('logout',views.log_out, name = 'log_out'),
    path('profile',views.user_profile, name = 'user_profile'),
    path('update',views.update, name = 'update'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:c_id>/', views.remove, name='remove'),
    path('hist-delete/<int:h_id>/', views.hremove, name='hremove'),
    path("update-quantity/", views.update_quantity, name="update_quantity"),
    path("checkout/", views.checkout, name="checkout"),
    path("order_history/", views.order_history, name="order_history"),
]