from django.db import models
from book.models import Book
from django.contrib.auth.models import  User



    

class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    items=models.ManyToManyField(Book)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)



# Create your models here.
# class UserProfile(models.Model):
    
#     fname=models.CharField(max_length=200)
#     lname=models.CharField(max_length=200)
#     username=models.CharField(max_length=200)
#     mob_no=models.CharField(max_length=30)
#     join_date=models.DateTimeField(auto_now_add=True)
    
#     image=models.ImageField(upload_to='profile_media')
#     password1=models.CharField(max_length=100)
#     password2=models.CharField(max_length=100)

#     def __str__(self) -> str:
#         return f"{self.username}"
    
# class LoginTable(models.Model):
#     username=models.CharField(max_length=200)
#     password1=models.CharField(max_length=100)
#     password2=models.CharField(max_length=100)
#     type=models.CharField(max_length=200)

#     def __str__(self) -> str:
#         return f"{self.username}"
    
