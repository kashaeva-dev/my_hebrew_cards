# Generated by Django 4.1.4 on 2022-12-27 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mycards", "0012_alter_topic_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="wordform",
            name="main_form",
        ),
    ]