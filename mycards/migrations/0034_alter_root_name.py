# Generated by Django 4.1.4 on 2023-01-23 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mycards", "0033_remove_word_unique_word_word_unique_word"),
    ]

    operations = [
        migrations.AlterField(
            model_name="root",
            name="name",
            field=models.CharField(
                max_length=15, unique=True, verbose_name="Подгруппа"
            ),
        ),
    ]
