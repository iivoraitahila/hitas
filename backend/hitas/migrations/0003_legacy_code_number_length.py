# Generated by Django 3.2.15 on 2022-08-18 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hitas", "0002_alter_apartment_share_number_start"),
    ]

    operations = [
        migrations.AlterField(
            model_name="apartmenttype",
            name="legacy_code_number",
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name="buildingtype",
            name="legacy_code_number",
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name="developer",
            name="legacy_code_number",
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name="financingmethod",
            name="legacy_code_number",
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name="postalcode",
            name="legacy_code_number",
            field=models.CharField(max_length=12, null=True),
        ),
    ]
