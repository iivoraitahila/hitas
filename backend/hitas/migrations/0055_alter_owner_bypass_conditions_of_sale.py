# Generated by Django 3.2.16 on 2023-02-07 10:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hitas", "0054_owner_bypass_conditions_of_sale"),
    ]

    operations = [
        migrations.AlterField(
            model_name="owner",
            name="bypass_conditions_of_sale",
            field=models.BooleanField(default=False),
        ),
    ]
