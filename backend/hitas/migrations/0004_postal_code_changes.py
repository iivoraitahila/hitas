# Generated by Django 3.2.15 on 2022-08-18 16:56

import uuid

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


def migrate_postal_codes(apps, schema_editor):
    PostalCode = apps.get_model("hitas", "PostalCode")
    HitasPostalCode = apps.get_model("hitas", "HitasPostalCode")
    for pc in PostalCode.objects.all():
        hpc = HitasPostalCode()
        hpc.id = pc.id
        hpc.value = hpc.value
        hpc.city = "Helsinki"
        hpc.cost_area = 1

        hpc.save()


def reverse_migrate_postal_codes(apps, schema_editor):
    HitasPostalCode = apps.get_model("hitas", "HitasPostalCode")
    HitasPostalCode.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("hitas", "0003_legacy_code_number_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="HitasPostalCode",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("value", models.CharField(max_length=5)),
                ("city", models.CharField(default="Helsinki", max_length=1024)),
                (
                    "cost_area",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MaxValueValidator(4),
                            django.core.validators.MinValueValidator(1),
                        ]
                    ),
                ),
            ],
            options={
                "verbose_name": "Postal code",
                "verbose_name_plural": "Postal codes",
            },
        ),
        migrations.RunPython(migrate_postal_codes, reverse_code=reverse_migrate_postal_codes),
        migrations.AddField(
            model_name="person",
            name="city",
            field=models.CharField(default="Helsinki", max_length=1024),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="propertymanager",
            name="city",
            field=models.CharField(default="Helsinki", max_length=1024),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="person",
            name="postal_code",
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name="propertymanager",
            name="postal_code",
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name="apartment",
            name="postal_code",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, related_name="apartments", to="hitas.hitaspostalcode"
            ),
        ),
        migrations.AlterField(
            model_name="building",
            name="postal_code",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, related_name="buildings", to="hitas.hitaspostalcode"
            ),
        ),
        migrations.AlterField(
            model_name="housingcompany",
            name="postal_code",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="housing_companies",
                to="hitas.hitaspostalcode",
            ),
        ),
        migrations.AlterField(
            model_name="realestate",
            name="postal_code",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, related_name="real_estates", to="hitas.hitaspostalcode"
            ),
        ),
        migrations.DeleteModel(
            name="PostalCode",
        ),
    ]
