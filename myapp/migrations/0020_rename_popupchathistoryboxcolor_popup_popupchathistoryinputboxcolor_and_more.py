# Generated by Django 4.2.1 on 2023-06-04 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_remove_popup_popupborderpadding_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='popup',
            old_name='popupChatHistoryBoxColor',
            new_name='popupChatHistoryInputBoxColor',
        ),
        migrations.RenameField(
            model_name='popup',
            old_name='popupChatHistoryFocusBorderColor',
            new_name='popupChatHistoryInputFocusBorderColor',
        ),
        migrations.AddField(
            model_name='popup',
            name='popupChatHistoryOutputBoxColor',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='popup',
            name='popupChatHistoryOutputFocusBorderColor',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
