# Generated by Django 3.1.5 on 2021-01-14 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=450)),
                ('discount', models.CharField(max_length=450)),
                ('image', models.ImageField(blank=True, upload_to='')),
            ],
        ),
    ]
