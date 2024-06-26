# Generated by Django 4.2.1 on 2024-03-27 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0004_subject_alter_teacher_full_name_alter_teacher_login_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Создайте группу', max_length=50, unique=True, verbose_name='Название группы')),
            ],
        ),
    ]
