# Generated by Django 3.2 on 2022-04-17 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helperapp', '0002_predict_grow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predict_grow',
            name='value',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
