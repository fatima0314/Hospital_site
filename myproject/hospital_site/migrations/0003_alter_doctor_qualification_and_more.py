# Generated by Django 5.1.4 on 2025-01-04 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_site', '0002_doctor_qualification_en_doctor_qualification_ru'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='qualification',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='qualification_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='qualification_ru',
            field=models.CharField(max_length=100, null=True),
        ),
    ]