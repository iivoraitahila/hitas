# Generated by Django 3.2.16 on 2022-11-21 12:07

import django.core.validators
from django.db import migrations, models

import hitas.models._base


def remove_zero_value_indices(apps, schema_editor):
    indices = [
        apps.get_model("hitas", "MaximumPriceIndex"),
        apps.get_model("hitas", "MarketPriceIndex"),
        apps.get_model("hitas", "MarketPriceIndex2005Equal100"),
        apps.get_model("hitas", "ConstructionPriceIndex"),
        apps.get_model("hitas", "ConstructionPriceIndex2005Equal100"),
        apps.get_model("hitas", "SurfaceAreaPriceCeiling"),
    ]

    for index in indices:
        index.objects.filter(value=0).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("hitas", "0038_bump_json_version"),
    ]

    operations = [
        migrations.AlterField(
            model_name="constructionpriceindex",
            name="value",
            field=hitas.models._base.HitasModelDecimalField(
                decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
        migrations.AlterField(
            model_name="constructionpriceindex2005equal100",
            name="value",
            field=hitas.models._base.HitasModelDecimalField(
                decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
        migrations.AlterField(
            model_name="marketpriceindex",
            name="value",
            field=hitas.models._base.HitasModelDecimalField(
                decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
        migrations.AlterField(
            model_name="marketpriceindex2005equal100",
            name="value",
            field=hitas.models._base.HitasModelDecimalField(
                decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
        migrations.AlterField(
            model_name="maximumpriceindex",
            name="value",
            field=hitas.models._base.HitasModelDecimalField(
                decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
        migrations.AlterField(
            model_name="surfaceareapriceceiling",
            name="value",
            field=hitas.models._base.HitasModelDecimalField(
                decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
        migrations.RunPython(remove_zero_value_indices, reverse_code=migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name="constructionpriceindex",
            constraint=models.CheckConstraint(
                check=models.Q(("value__gt", 0)), name="construction_price_index_value_positive"
            ),
        ),
        migrations.AddConstraint(
            model_name="constructionpriceindex2005equal100",
            constraint=models.CheckConstraint(
                check=models.Q(("value__gt", 0)), name="construction_price_2005_index_value_positive"
            ),
        ),
        migrations.AddConstraint(
            model_name="marketpriceindex",
            constraint=models.CheckConstraint(
                check=models.Q(("value__gt", 0)), name="market_price_index_value_positive"
            ),
        ),
        migrations.AddConstraint(
            model_name="marketpriceindex2005equal100",
            constraint=models.CheckConstraint(
                check=models.Q(("value__gt", 0)), name="market_price_2005_index_value_positive"
            ),
        ),
        migrations.AddConstraint(
            model_name="maximumpriceindex",
            constraint=models.CheckConstraint(
                check=models.Q(("value__gt", 0)), name="maximum_price_index_value_positive"
            ),
        ),
    ]
