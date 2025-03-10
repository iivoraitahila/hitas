# Generated by Django 3.2.15 on 2022-09-09 08:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hitas", "0015_housing_company_cascade"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="apartment",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(("share_number_end__isnull", False), ("share_number_start__isnull", False)),
                    models.Q(("share_number_end__isnull", True), ("share_number_start__isnull", True)),
                    _connector="OR",
                ),
                name="hitas_apartment_share_number_both_set",
            ),
        ),
    ]
