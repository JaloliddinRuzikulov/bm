# Generated by Django 4.1.4 on 2022-12-27 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depot',
            name='came_out_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]