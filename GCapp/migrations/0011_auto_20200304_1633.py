# Generated by Django 3.0.3 on 2020-03-04 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GCapp', '0010_auto_20200304_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='games',
            name='game_introduction',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='games',
            name='game_rules',
            field=models.TextField(),
        ),
    ]
