# Generated by Django 5.1.3 on 2024-11-11 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bitcoin',
            name='purchased_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='silver',
            name='purchased_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='stock',
            name='purchased_at',
            field=models.DateTimeField(),
        ),
    ]
