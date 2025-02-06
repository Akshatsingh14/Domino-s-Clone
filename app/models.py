from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth.models import User
import random
from django.utils.timezone import now, timedelta

# Create your models here.
class R_image(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='round/', storage=FileSystemStorage(location=settings.MEDIA_ROOT))  # Images will be saved in MEDIA_ROOT/round/
    order = models.IntegerField(default=0)  # Adding an order field to specify custom sorting

    def __str__(self):
        return self.name
    
class Slide_img(models.Model):
    image = models.ImageField(upload_to='slide/', storage=FileSystemStorage(location=settings.MEDIA_ROOT))
    order = models.IntegerField(default=0)  
    
    def __str__(self):
        if self.image:
            return f"Image: {self.image.name}"  # Access the filename
        else:
            return "No Image"
        
class Bestsell(models.Model):
    image = models.ImageField(upload_to='bestseller/', storage=FileSystemStorage(location=settings.MEDIA_ROOT))
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=300)
    price = models.IntegerField()
    order = models.IntegerField(default=0)  
    
    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_img = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_email(self):
        return self.user.email
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Bestsell, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.item.name}"

    def get_total_price(self):
        return self.quantity * self.item.price  
    
class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Bestsell, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  # Store quantity at checkout
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Store total price at checkout
    image = models.ImageField(upload_to='order_images/', blank=True, null=True)  # Store item image
    order_date = models.DateTimeField(auto_now_add=True)  # Timestamp of the order

    def __str__(self):
        return f"{self.user.username} - {self.item.name} - {self.order_date}"