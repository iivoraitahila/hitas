# Generated by Django 3.2.16 on 2022-10-07 13:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("hitas", "0027_surfaceareapriceceiling"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="housingcompany",
            name="realized_acquisition_price_positive",
        ),
        migrations.RemoveField(
            model_name="housingcompany",
            name="realized_acquisition_price",
        ),
    ]
