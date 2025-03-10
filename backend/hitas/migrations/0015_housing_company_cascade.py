# Generated by Django 3.2.15 on 2022-09-07 09:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hitas", "0014_soft_delete"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ownership",
            name="apartment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="ownerships", to="hitas.apartment"
            ),
        ),
        migrations.AlterField(
            model_name="apartment",
            name="building",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="apartments", to="hitas.building"
            ),
        ),
        migrations.AlterField(
            model_name="building",
            name="real_estate",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="buildings", to="hitas.realestate"
            ),
        ),
        migrations.AlterField(
            model_name="realestate",
            name="housing_company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="real_estates", to="hitas.housingcompany"
            ),
        ),
    ]
