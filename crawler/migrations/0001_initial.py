# Generated by Django 3.2.7 on 2021-10-27 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('deal_price', models.FloatField()),
                ('seller', models.CharField(max_length=255)),
                ('main_price', models.FloatField(null=True)),
                ('stars', models.FloatField()),
                ('count', models.IntegerField()),
                ('image', models.CharField(max_length=1000)),
                ('create', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crawler.product')),
            ],
        ),
    ]