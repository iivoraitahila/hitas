# Generated by Django 3.2.16 on 2022-10-06 09:45

from decimal import Decimal

import django.core.validators
from django.db import migrations, models

import hitas.models._base


class Migration(migrations.Migration):
    dependencies = [
        ("hitas", "0026_housing_company_required_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="SurfaceAreaPriceCeiling",
            fields=[
                ("month", models.DateField(primary_key=True, serialize=False)),
                (
                    "value",
                    hitas.models._base.HitasModelDecimalField(
                        decimal_places=2,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                    ),
                ),
            ],
            options={
                "verbose_name": "Surface area price ceiling",
                "verbose_name_plural": "Surface area price ceiling",
            },
        ),
    ]
