from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


User=get_user_model()

class limit_val(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    limit_id=models.AutoField(primary_key=True)
    limit = models.IntegerField()
    def __str__(self):
        return self.user.username + ' has set a limit of Rupee : ' + str(self.limit)

class expense(models.Model):
    payChoice=(
        ('cash','cash'),
        ('creditcard','creditcard'),
        ('debitcard','debitcard'),
        ('upi','upi'),
        ('onlinebanking','onlinebanking'),
    )
    categoryChoice=(
        ('food','food'),
        ('entertainment','entertainment'),
        ('stocks','stocks'),
        ('rent','rent'),
        ('emi','emi'),
        ('others','others'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exp_name = models.CharField(max_length=100)
    amount = models.IntegerField()
    exp_id=models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True,editable=False,blank=True)
    category=models.CharField(max_length=100,choices=categoryChoice,default='others')
    pay_mode=models.CharField(max_length=100,choices=payChoice,default='cash')
    
    def __str__(self):
        return self.exp_name + ' for Rupee  : ' + str(self.amount)

