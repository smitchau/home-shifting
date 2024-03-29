# Generated by Django 5.0 on 2024-03-12 10:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Truckpartner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_name', models.CharField(max_length=30)),
                ('t_email', models.EmailField(max_length=30, unique=True)),
                ('t_password', models.CharField(max_length=20)),
                ('t_contact', models.CharField(max_length=11, unique=True)),
                ('t_rcnumber', models.CharField(max_length=50, unique=True)),
                ('t_aadharcard_details', models.CharField(max_length=30, unique=True)),
                ('t_pancard_details', models.CharField(max_length=30, unique=True)),
                ('t_drivinglicence_details', models.CharField(max_length=30, unique=True)),
                ('t_picture', models.ImageField(default='images/pic-1.jpg', upload_to='images/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
    ]
