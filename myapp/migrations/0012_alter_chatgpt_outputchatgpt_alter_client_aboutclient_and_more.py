# Generated by Django 4.2.1 on 2023-05-24 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_alter_chatgpt_requestid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatgpt',
            name='outputChatGPT',
            field=models.TextField(max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='aboutClient',
            field=models.TextField(max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='helpPage',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='website',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='clientproducts',
            name='productDetails',
            field=models.TextField(max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='clientproducts',
            name='productLink',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='clientproducts',
            name='productPrice',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='clientproducts',
            name='productPriceWithPromo',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='popup',
            name='popupContent',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='popup',
            name='popupTitle',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='popupengagement',
            name='popupEngagementEnd',
            field=models.DateTimeField(null=True),
        ),
    ]
