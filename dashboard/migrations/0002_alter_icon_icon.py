# Generated by Django 5.0 on 2023-12-21 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='icon',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='shopicons/'),
        ),
    ]