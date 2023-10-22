# Generated by Django 4.2.6 on 2023-10-22 11:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="score_count",
            field=models.PositiveIntegerField(default=0, verbose_name="Score count"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="score_sum",
            field=models.PositiveBigIntegerField(default=0, verbose_name="Score sum"),
            preserve_default=False,
        ),
    ]
