# Generated by Django 3.2 on 2021-10-31 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='privacy',
            field=models.CharField(choices=[('Public', 'Public'), ('Friends', 'Friends'), ('Onlyme', 'Onlyme')], default='Public', max_length=9),
        ),
    ]
