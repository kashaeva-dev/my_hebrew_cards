# Generated by Django 4.1.4 on 2023-01-19 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mycards", "0030_alter_wordform_gender_alter_wordform_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="word",
            name="animacy",
            field=models.BooleanField(
                blank=True, default=False, null=True, verbose_name="Одушевленность"
            ),
        ),
    ]
