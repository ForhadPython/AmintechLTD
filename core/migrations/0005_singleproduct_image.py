# Generated by Django 3.1.5 on 2021-01-14 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_singleproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='singleproduct',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
