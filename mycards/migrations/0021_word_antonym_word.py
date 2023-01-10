# Generated by Django 4.1.4 on 2023-01-03 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mycards", "0020_word_is_antonym"),
    ]

    operations = [
        migrations.AddField(
            model_name="word",
            name="antonym_word",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="antonym",
                to="mycards.word",
                verbose_name="Антоним",
            ),
        ),
    ]