# Generated by Django 3.2.15 on 2022-09-29 13:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hitas", "0023_indices"),
    ]

    operations = [
        migrations.RenameModel("Person", "Owner"),
        migrations.RunSQL("UPDATE hitas_owner SET first_name = first_name || ' ' || last_name"),
        migrations.RenameField("Owner", "first_name", "name"),
        migrations.RemoveField("Owner", "last_name"),
        migrations.RenameField("Owner", "social_security_number", "identifier"),
        migrations.AlterModelOptions(
            name="owner",
            options={"ordering": ["id"], "verbose_name": "Owner", "verbose_name_plural": "Owners"},
        ),
        migrations.AlterField(
            model_name="owner",
            name="name",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
