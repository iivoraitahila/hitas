# Generated by Django 3.2.16 on 2023-02-07 07:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hitas", "0053_remove_start_and_end_date_from_ownership"),
    ]

    operations = [
        migrations.AddField(
            model_name="owner",
            name="bypass_conditions_of_sale",
            field=models.BooleanField(default=True),
        ),
    ]
