# Generated by Django 4.2.1 on 2023-06-25 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0037_chatgpt_chatwebsiteurl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='code',
            name='user',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Code',
        ),
    ]