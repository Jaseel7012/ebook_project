from django.db import models

# Create your models here.
class Author(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.name}"
    
class Book(models.Model):
    title=models.CharField(max_length=200)
    author=models.ForeignKey(Author,on_delete=models.CASCADE)
    serial_no=models.CharField(max_length=200)
    publish_date=models.DateField()
    quantity=models.IntegerField()
    price=models.IntegerField()
    image=models.ImageField(upload_to='book_media')

    def __str__(self) -> str:
        return f"{self.title}"