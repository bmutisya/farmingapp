# Generated by Django 5.0.1 on 2024-02-17 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_animalhealth'),
    ]

    operations = [
        migrations.RenameField(
            model_name='animalhealth',
            old_name='diagonisis',
            new_name='diagnosis',
        ),
    ]
