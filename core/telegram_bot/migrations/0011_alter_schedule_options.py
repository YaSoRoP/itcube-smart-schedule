# Generated by Django 4.2.1 on 2024-03-28 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0010_schedule'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schedule',
            options={'verbose_name': 'Занятие', 'verbose_name_plural': 'Занятия'},
        ),
    ]
