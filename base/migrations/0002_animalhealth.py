# Generated by Django 5.0.1 on 2024-02-17 07:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnimalHealth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('symptoms', models.TextField(blank=True, null=True)),
                ('diagonisis', models.TextField(blank=True, null=True)),
                ('treatment', models.TextField(blank=True, null=True)),
                ('cost', models.CharField(blank=True, max_length=100, null=True)),
                ('vet_name', models.CharField(max_length=100)),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.animal')),
            ],
        ),
    ]
