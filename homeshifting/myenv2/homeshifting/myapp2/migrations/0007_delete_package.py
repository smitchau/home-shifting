# Generated by Django 5.0 on 2024-03-14 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp2', '0006_remove_package_end_date_remove_package_package_name_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Package',
        ),
    ]
