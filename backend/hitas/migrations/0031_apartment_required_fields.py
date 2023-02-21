# Generated by Django 3.2.15 on 2022-10-17 08:05

from decimal import Decimal

import django.core.validators
import enumfields.fields
from django.db import migrations, models

import hitas.models._base
import hitas.models.apartment


class Migration(migrations.Migration):
    dependencies = [
        ("hitas", "0030_apartment_rooms"),
    ]

    operations = [
        migrations.RenameField(
            model_name="apartment",
            old_name="second_purchase_date",
            new_name="latest_purchase_date",
        ),
        migrations.AlterField(
            model_name="apartment",
            name="additional_work_during_construction",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="apartment",
            name="debt_free_purchase_price",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="apartment",
            name="debt_free_purchase_price_during_construction",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="apartment",
            name="interest_during_construction",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="apartment",
            name="loans_during_construction",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="apartment",
            name="primary_loan_amount",
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name="apartment",
            name="state",
            field=enumfields.fields.EnumField(
                default="free", enum=hitas.models.apartment.ApartmentState, max_length=10, null=True
            ),
        ),
        migrations.AlterField(
            model_name="apartment",
            name="surface_area",
            field=hitas.models._base.HitasModelDecimalField(
                decimal_places=2,
                help_text="Measured in m^2",
                max_digits=15,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
            ),
        ),
    ]
