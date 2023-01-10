# Generated by Django 4.1.4 on 2023-01-01 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mycards", "0013_remove_wordform_main_form"),
    ]

    operations = [
        migrations.CreateModel(
            name="Expression",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "expression",
                    models.CharField(max_length=256, verbose_name="Выражение"),
                ),
                (
                    "translation",
                    models.CharField(max_length=256, verbose_name="Перевод"),
                ),
                (
                    "pronunciation",
                    models.CharField(max_length=256, verbose_name="Произношение"),
                ),
                (
                    "topic",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="expressions",
                        to="mycards.topic",
                        verbose_name="Тема",
                    ),
                ),
                (
                    "word",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="expressions",
                        to="mycards.word",
                        verbose_name="Основная форма",
                    ),
                ),
            ],
        ),
    ]