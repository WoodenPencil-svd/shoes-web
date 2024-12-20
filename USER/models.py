from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    realname = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    address = models.CharField(null=True, max_length=200, blank=True)
    city = models.ManyToManyField('City', blank=True) 
    phonenumber = models.CharField(max_length=11 , null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.user)
    
    
    from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
