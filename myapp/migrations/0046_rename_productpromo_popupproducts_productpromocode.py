# Generated by Django 4.2.1 on 2023-07-01 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0045_popupproducts_productcurrency'),
    ]

    operations = [
        migrations.RenameField(
            model_name='popupproducts',
            old_name='productPromo',
            new_name='productPromoCode',
        ),
    ]
