# Generated by Django 3.2.7 on 2021-10-27 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0002_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(max_length=25, null=True),
        ),
    ]