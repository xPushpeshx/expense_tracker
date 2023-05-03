from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from datetime import datetime

User=get_user_model()

class limit_val(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    limit_id=models.AutoField(primary_key=True)
    limit = models.IntegerField()
    def __str__(self):
        return self.user.username + ' has set a limit of Rupee : ' + str(self.limit)
    
class daily(models.Model):
    daily_exp=models.CharField(max_length=62, default='0,'*30+'0')
    daily_id=models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def record_daily_expense(self, amount):
        # Get today's date
        today = datetime.today()
        # Get the index for today's date (1-31)
        index = today.day - 1
        # Split the zeros string into a list of integers
        zeros_array= [int(x) for x in self.daily_exp.split(',')]
        if zeros_array[index] != 0:
            # If an expense has already been recorded, add the new amount to it
            zeros_array[index] += int(amount)
        else:
            # If no expense has been recorded yet for today, set the expense to the new amount
            zeros_array[index] = int(amount)
        # Add the amount to the expense for today
        # Convert the modified zeros array back to a string
        zeros_string = ','.join(str(x) for x in zeros_array)
        # Save the modified zeros string to the model instance
        self.daily_exp = zeros_string
        self.save()
    
class month(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month_id=models.AutoField(primary_key=True)
    month_name = models.CharField(max_length=100)
    total_expense=models.IntegerField(default=0)
    total_limit=models.IntegerField(default=0)
    def __str__(self):
        return self.user.username + ' has set a month : ' + str(self.month_name)
    
class year(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year_id=models.AutoField(primary_key=True)
    year_name = models.CharField(max_length=100)
    total_expense=models.IntegerField(default=0)
    total_limit=models.IntegerField(default=0)
    def __str__(self):
        return self.user.username + ' has set a year : ' + str(self.year_name)

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
    date = models.DateField(auto_now_add=True,editable=True)
    category=models.CharField(max_length=100,choices=categoryChoice,default='others')
    pay_mode=models.CharField(max_length=100,choices=payChoice,default='cash')
    
    def __str__(self):
        return self.exp_name + ' for Rupee  : ' + str(self.amount)

