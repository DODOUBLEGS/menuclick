# Generated by Django 5.0 on 2024-02-03 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_alter_icon_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='menu_brochure',
            field=models.FileField(default=1, upload_to='menu_brochures/', verbose_name='Menu / Brochure'),
            preserve_default=False,
        ),
    ]