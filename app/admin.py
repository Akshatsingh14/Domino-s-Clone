from django.contrib import admin
from .models import R_image, Slide_img, Bestsell, Cart

# Register your models here.
@admin.register(R_image)
class RoundAdmin(admin.ModelAdmin):
    list_display = ('name','image','order')
    list_editable = ('order',)  # Make the order field editable directly in the admin
    
@admin.register(Slide_img)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('image','order')
    list_editable = ('order',)
    
@admin.register(Bestsell)
class SellAdmin(admin.ModelAdmin):
    list_display = ('name','image', 'price','order')
    list_editable = ('order',)
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('item','quantity')
    list_editable = ('quantity',)