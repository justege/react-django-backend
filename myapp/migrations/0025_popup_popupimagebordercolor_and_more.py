# Generated by Django 4.2.1 on 2023-06-06 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0024_popup_popupimageheight_popup_popupimagewidth'),
    ]

    operations = [
        migrations.AddField(
            model_name='popup',
            name='popupImageBorderColor',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='popup',
            name='popupImageBorderWidth',
            field=models.CharField(max_length=4, null=True),
        ),
    ]
