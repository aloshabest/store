# Generated by Django 4.1.1 on 2022-09-23 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazine', '0003_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default=None, upload_to='photo/%Y/%m/%d', verbose_name='Фото'),
        ),
    ]