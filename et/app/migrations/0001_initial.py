# Generated by Django 4.2 on 2023-04-23 16:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='person',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='expense',
            fields=[
                ('exp_name', models.CharField(max_length=100)),
                ('amount', models.IntegerField()),
                ('exp_id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(auto_now=True)),
                ('category', models.CharField(choices=[('food', 'food'), ('entertainment', 'entertainment'), ('stocks', 'stocks'), ('rent', 'rent'), ('emi', 'emi'), ('others', 'others')], default='others', max_length=100)),
                ('pay_mode', models.CharField(choices=[('cash', 'cash'), ('creditcard', 'creditcard'), ('debitcard', 'debitcard'), ('upi', 'upi'), ('onlinebanking', 'onlinebanking')], default='cash', max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.person')),
            ],
        ),
    ]