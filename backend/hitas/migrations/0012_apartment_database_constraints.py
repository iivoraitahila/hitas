# Generated by Django 3.2.15 on 2022-08-31 06:30

import django.db.models.expressions
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hitas", "0011_apartment_prices_update"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="apartment",
            constraint=models.CheckConstraint(
                check=models.Q(("share_number_start__gte", 1)), name="hitas_apartment_share_number_start_gte_1"
            ),
        ),
        migrations.AddConstraint(
            model_name="apartment",
            constraint=models.CheckConstraint(
                check=models.Q(("share_number_end__gte", 1)), name="hitas_apartment_share_number_end_gte_1"
            ),
        ),
        migrations.AddConstraint(
            model_name="apartment",
            constraint=models.CheckConstraint(
                check=models.Q(("share_number_end__gte", django.db.models.expressions.F("share_number_start"))),
                name="hitas_apartment_share_number_start_lte_share_number_end",
            ),
        ),
        migrations.AddConstraint(
            model_name="apartment",
            constraint=models.CheckConstraint(
                check=models.Q(("surface_area__gte", 0)), name="hitas_apartment_surface_area_gte_0"
            ),
        ),
    ]
