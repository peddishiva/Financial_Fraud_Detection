from django.db import models

# Create your models here.
from django.db.models import CASCADE


class ClientRegister_Model(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address= models.CharField(max_length=3000)
    gender= models.CharField(max_length=30)

class detect_financial_fraud(models.Model):

    Fid= models.CharField(max_length=3000)
    trans_datetime= models.CharField(max_length=3000)
    Acc_num= models.CharField(max_length=3000)
    bankingtype= models.CharField(max_length=3000)
    category= models.CharField(max_length=3000)
    amt= models.CharField(max_length=3000)
    Name= models.CharField(max_length=3000)
    gender= models.CharField(max_length=3000)
    street= models.CharField(max_length=3000)
    city= models.CharField(max_length=3000)
    zip= models.CharField(max_length=3000)
    lat= models.CharField(max_length=3000)
    lon= models.CharField(max_length=3000)
    job= models.CharField(max_length=3000)
    dob= models.CharField(max_length=3000)
    trans_num= models.CharField(max_length=3000)
    merch_lat= models.CharField(max_length=3000)
    merch_long= models.CharField(max_length=3000)
    Prediction= models.CharField(max_length=3000)

class detection_accuracy(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)

class detection_ratio(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)



