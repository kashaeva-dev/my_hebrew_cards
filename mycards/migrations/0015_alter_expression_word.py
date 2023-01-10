# Generated by Django 4.1.4 on 2023-01-02 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mycards", "0014_expression"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expression",
            name="word",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="expressions",
                to="mycards.wordform",
                verbose_name="Основная форма",
            ),
        ),
    ]