# Generated by Django 4.2.6 on 2023-10-22 15:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_user_score_count_alter_user_score_sum"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="register_code",
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
