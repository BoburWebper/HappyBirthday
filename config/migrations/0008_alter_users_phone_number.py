# Generated by Django 5.0.6 on 2024-05-28 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0007_remove_userbirthdays_images_userbirthdayimages_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='phone_number',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]
