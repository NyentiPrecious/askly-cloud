# Generated by Django 5.2.2 on 2025-07-09 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0004_question_allow_multiple_question_ype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='ype',
            new_name='type',
        ),
    ]
