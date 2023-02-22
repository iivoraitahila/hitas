# Generated by Django 3.2.16 on 2023-01-23 10:36

import uuid

import django.db.models.deletion
import django.db.models.expressions
import enumfields.fields
from django.db import migrations, models

import hitas.models.condition_of_sale


class Migration(migrations.Migration):
    dependencies = [
        ("hitas", "0050_change_apartment_sale_statistics_field_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="ConditionOfSale",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("deleted", models.DateTimeField(db_index=True, editable=False, null=True)),
                ("deleted_by_cascade", models.BooleanField(default=False, editable=False)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                (
                    "grace_period",
                    enumfields.fields.EnumField(
                        default="not_given", enum=hitas.models.condition_of_sale.GracePeriod, max_length=12
                    ),
                ),
                (
                    "new_ownership",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="conditions_of_sale_new",
                        to="hitas.ownership",
                    ),
                ),
                (
                    "old_ownership",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="conditions_of_sale_old",
                        to="hitas.ownership",
                    ),
                ),
            ],
            options={
                "verbose_name": "Condition of Sale",
                "verbose_name_plural": "Conditions of Sale",
                "ordering": ["id"],
            },
        ),
        migrations.AddField(
            model_name="ownership",
            name="conditions_of_sale",
            field=models.ManyToManyField(through="hitas.ConditionOfSale", to="hitas.Ownership"),
        ),
        migrations.AddConstraint(
            model_name="conditionofsale",
            constraint=models.CheckConstraint(
                check=models.Q(("new_ownership", django.db.models.expressions.F("old_ownership")), _negated=True),
                name="hitas_conditionofsale_no_circular_reference",
            ),
        ),
        migrations.AddConstraint(
            model_name="conditionofsale",
            constraint=models.UniqueConstraint(
                condition=models.Q(("deleted__isnull", True)),
                fields=("new_ownership", "old_ownership"),
                name="hitas_conditionofsale_only_one_valid_condition_of_sale",
            ),
        ),
    ]
