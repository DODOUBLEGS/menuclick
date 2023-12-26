# Generated by Django 5.0 on 2023-12-21 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_remove_icon_icon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='social_icons',
        ),
        migrations.RemoveField(
            model_name='shop',
            name='social_icons_url',
        ),
        migrations.AddField(
            model_name='icon',
            name='social_icons_url',
            field=models.URLField(blank=True, null=True, verbose_name='Social Icons Url'),
        ),
    ]