# Generated by Django 3.0.2 on 2020-11-09 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20201109_0437'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='ut1pb',
            field=models.ImageField(blank=True, upload_to='plots'),
        ),
        migrations.AddField(
            model_name='profile',
            name='ut2pb',
            field=models.ImageField(blank=True, upload_to='plots'),
        ),
        migrations.AddField(
            model_name='profile',
            name='ut3pb',
            field=models.ImageField(blank=True, upload_to='plots'),
        ),
    ]
