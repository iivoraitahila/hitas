# Generated by Django 3.2.16 on 2022-11-04 06:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hitas", "0033_max_to_maximum"),
    ]

    operations = [
        migrations.CreateModel(
            name="MigrationDone",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("when", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
