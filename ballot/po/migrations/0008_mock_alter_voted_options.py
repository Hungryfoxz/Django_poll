# Generated by Django 4.0.2 on 2022-06-14 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('po', '0007_voted'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('position', models.CharField(choices=[('Position-1', 'Posiotion-1'), ('Position-2', 'Position-2'), ('Position-3', 'Position-3'), ('Position-4', 'Position-4'), ('Position-5', 'Position-5')], max_length=25)),
                ('image', models.ImageField(upload_to='templates/images/')),
                ('votes', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Mock Poll Table',
            },
        ),
        migrations.AlterModelOptions(
            name='voted',
            options={'verbose_name_plural': 'Zone_Total_Students_Voted'},
        ),
    ]
