from django.db import models
import uuid
from django.contrib.auth.models import User


class Shoes(models.Model):
    name = models.CharField(max_length=100, null= None, blank= None)
    tag = models.ManyToManyField('Tag')
    image = models.ImageField(upload_to='shoesImage/', null=True, blank=True)
    description = models.TextField(max_length=500)
    id = models.CharField(max_length=100, default=uuid.uuid4,unique=True,primary_key= True,editable= False)
    size = models.ManyToManyField('SizeShoe')
    price = models.CharField(max_length=20, null= None, blank= None)
    brand = models.ManyToManyField('Brand')
    
    
    def __str__(self):
        return str(self.name)
    
    
class Tag(models.Model):
    name = models.CharField(max_length= 20)
    slug = models.SlugField(max_length=20, unique=True)
    def __str__(self):
        return str(self.name)
    
class SizeShoe(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return str(self.name)
    
class Brand(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)
    def __str__(self):
        return str(self.name)


    
    
    

    
    





     
     
    

