from django.db import models

# Create your models here.

class getLinkData(models.Model):

    link_name = models.CharField(max_length=5000,null=True,blank=True)
    link_address = models.CharField(max_length=5000,null=True,blank=True)