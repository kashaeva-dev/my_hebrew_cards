# Generated by Django 4.1.4 on 2022-12-19 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mycards", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="root",
            name="binyan",
        ),
        migrations.RemoveField(
            model_name="root",
            name="picture",
        ),
        migrations.RemoveField(
            model_name="word",
            name="example",
        ),
        migrations.RemoveField(
            model_name="word",
            name="exception",
        ),
        migrations.RemoveField(
            model_name="word",
            name="pronunciation",
        ),
        migrations.RemoveField(
            model_name="word",
            name="translation",
        ),
        migrations.RemoveField(
            model_name="word",
            name="vocal_name",
        ),
        migrations.AddField(
            model_name="word",
            name="binyan",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="mycards.binyan",
                verbose_name="Биньян с подгруппой",
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="WordForm",
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
                    "name",
                    models.CharField(
                        max_length=64, verbose_name="Название (для поиска)"
                    ),
                ),
                (
                    "vocal_name",
                    models.CharField(
                        max_length=64, verbose_name="Название с огласовками"
                    ),
                ),
                ("exception", models.BooleanField(default=False)),
                (
                    "pronunciation",
                    models.CharField(max_length=64, verbose_name="Произношение"),
                ),
                (
                    "translation",
                    models.CharField(max_length=64, verbose_name="Перевод"),
                ),
                ("example", models.TextField(null=True)),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="mycards.type",
                        verbose_name="Часть речи",
                    ),
                ),
                (
                    "word",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="forms",
                        to="mycards.word",
                        verbose_name="Основная форма",
                    ),
                ),
            ],
        ),
    ]
