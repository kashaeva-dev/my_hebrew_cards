# Generated by Django 4.1.4 on 2023-05-21 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycards', '0034_alter_root_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='root',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='root',
            name='name',
            field=models.CharField(max_length=15, unique=True, verbose_name='Корень'),
        ),
        migrations.AlterModelTable(
            name='word',
            table=None,
        ),
    ]
