# Generated by Django 3.2 on 2022-05-15 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helperapp', '0004_auto_20220418_0046'),
    ]

    operations = [
        migrations.AddField(
            model_name='predict_grow',
            name='time_close',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
