# Generated by Django 4.1.4 on 2022-12-24 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mycards", "0004_word_printed"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="wordform",
            name="type",
        ),
        migrations.AddField(
            model_name="wordform",
            name="gender",
            field=models.CharField(max_length=6, null=True),
        ),
        migrations.AddField(
            model_name="wordform",
            name="number",
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name="wordform",
            name="time",
            field=models.CharField(max_length=20, null=True),
        ),
    ]
