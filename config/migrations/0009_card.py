# Generated by Django 5.0.6 on 2024-05-29 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0008_alter_users_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardInfo', models.TextField(null=True)),
            ],
        ),
    ]