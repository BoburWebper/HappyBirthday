# Generated by Django 5.0.6 on 2024-05-28 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0005_alter_advertisement_image_alter_advertisement_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/birthday/')),
            ],
        ),
        migrations.RemoveField(
            model_name='userbirthdays',
            name='image',
        ),
        migrations.AddField(
            model_name='userbirthdays',
            name='images',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_birthdays', to='config.userimage'),
        ),
    ]