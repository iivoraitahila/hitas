# Generated by Django 3.2.16 on 2023-01-09 07:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hitas", "0046_interest_during_construction_split"),
    ]

    operations = [
        migrations.AlterField(
            model_name="apartment",
            name="building",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="apartments",
                to="hitas.building",
            ),
        ),
        migrations.AlterField(
            model_name="building",
            name="real_estate",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="buildings",
                to="hitas.realestate",
            ),
        ),
        migrations.AlterField(
            model_name="realestate",
            name="housing_company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="real_estates",
                to="hitas.housingcompany",
            ),
        ),
    ]
