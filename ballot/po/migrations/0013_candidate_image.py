# Generated by Django 4.0.2 on 2022-07-13 16:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('po', '0012_rename_voted_voted_voted_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='static/'),
            preserve_default=False,
        ),
    ]
