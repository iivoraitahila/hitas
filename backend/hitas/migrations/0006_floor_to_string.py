# Generated by Django 3.2.15 on 2022-08-22 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hitas", "0005_unique_postal_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="apartment",
            name="floor",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
