# Generated by Django 4.0.2 on 2022-06-09 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('po', '0003_extra_field_delete_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extra_field',
            options={'verbose_name_plural': 'zzz : donot_edit_anything_here'},
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='votes',
        ),
        migrations.AddField(
            model_name='candidate',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]