# Generated by Django 3.2.15 on 2022-09-28 15:19

from decimal import Decimal

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import hitas.models._base
import hitas.models.utils


class Migration(migrations.Migration):

    dependencies = [
        ("hitas", "0025_indices_update"),
    ]

    operations = [
        migrations.AlterField(
            model_name="housingcompany",
            name="business_id",
            field=models.CharField(
                null=True,
                help_text="Format: 1234567-8",
                max_length=9,
                validators=[hitas.models.utils.validate_business_id],
            ),
        ),
        migrations.AlterField(
            model_name="housingcompany",
            name="primary_loan",
            field=hitas.models._base.HitasModelDecimalField(
                blank=True,
                decimal_places=2,
                max_digits=15,
                null=True,
                validators=[django.core.validators.MinValueValidator(Decimal("0"))],
            ),
        ),
        migrations.AlterField(
            model_name="housingcompany",
            name="property_manager",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="housing_companies",
                to="hitas.propertymanager",
            ),
        ),
    ]
