# Generated by Django 3.2.15 on 2022-09-30 09:31

from decimal import Decimal

import django.core.validators
from django.db import migrations, models

import hitas.models._base


class Migration(migrations.Migration):
    dependencies = [
        ("hitas", "0022_legacy_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="ConstructionPriceIndex",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(db_index=True, editable=False, null=True)),
                ("deleted_by_cascade", models.BooleanField(default=False, editable=False)),
                (
                    "value",
                    hitas.models._base.HitasModelDecimalField(
                        decimal_places=2,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                    ),
                ),
                ("month", models.DateField()),
            ],
            options={
                "verbose_name": "Construction price index year for apartments constructed in January 2005 and after",
                "verbose_name_plural": (
                    "Construction price indices for apartments constructed in January 2005 and after"
                ),
            },
        ),
        migrations.CreateModel(
            name="ConstructionPriceIndexPre2005",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(db_index=True, editable=False, null=True)),
                ("deleted_by_cascade", models.BooleanField(default=False, editable=False)),
                (
                    "value",
                    hitas.models._base.HitasModelDecimalField(
                        decimal_places=2,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                    ),
                ),
                ("month", models.DateField()),
            ],
            options={
                "verbose_name": "Construction price index for apartments constructed before January 2005",
                "verbose_name_plural": "Construction price indices for apartments constructed before January 2005",
            },
        ),
        migrations.CreateModel(
            name="MarketPriceIndex",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(db_index=True, editable=False, null=True)),
                ("deleted_by_cascade", models.BooleanField(default=False, editable=False)),
                (
                    "value",
                    hitas.models._base.HitasModelDecimalField(
                        decimal_places=2,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                    ),
                ),
                ("month", models.DateField()),
            ],
            options={
                "verbose_name": "Market price index for apartments constructed in January 2005 or after",
                "verbose_name_plural": "Market price indices for apartment constructed in January 2005 or after",
            },
        ),
        migrations.CreateModel(
            name="MarketPriceIndexPre2005",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(db_index=True, editable=False, null=True)),
                ("deleted_by_cascade", models.BooleanField(default=False, editable=False)),
                (
                    "value",
                    hitas.models._base.HitasModelDecimalField(
                        decimal_places=2,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                    ),
                ),
                ("month", models.DateField()),
            ],
            options={
                "verbose_name": "Market price index for apartments constructed before January 2005",
                "verbose_name_plural": "Market price indices for apartment constructed before January 2005",
            },
        ),
        migrations.CreateModel(
            name="MaxPriceIndex",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(db_index=True, editable=False, null=True)),
                ("deleted_by_cascade", models.BooleanField(default=False, editable=False)),
                (
                    "value",
                    hitas.models._base.HitasModelDecimalField(
                        decimal_places=2,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                    ),
                ),
                ("month", models.DateField()),
            ],
            options={
                "verbose_name": "Max price index",
                "verbose_name_plural": "Max price indices",
            },
        ),
    ]
