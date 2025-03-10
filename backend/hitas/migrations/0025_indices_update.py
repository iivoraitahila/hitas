# Generated by Django 3.2.15 on 2022-09-30 13:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hitas", "0024_rename_person_to_owner"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="constructionpriceindex",
            name="deleted",
        ),
        migrations.RemoveField(
            model_name="constructionpriceindex",
            name="deleted_by_cascade",
        ),
        migrations.RemoveField(
            model_name="constructionpriceindex",
            name="id",
        ),
        migrations.RemoveField(
            model_name="constructionpriceindexpre2005",
            name="deleted",
        ),
        migrations.RemoveField(
            model_name="constructionpriceindexpre2005",
            name="deleted_by_cascade",
        ),
        migrations.RemoveField(
            model_name="constructionpriceindexpre2005",
            name="id",
        ),
        migrations.RemoveField(
            model_name="marketpriceindex",
            name="deleted",
        ),
        migrations.RemoveField(
            model_name="marketpriceindex",
            name="deleted_by_cascade",
        ),
        migrations.RemoveField(
            model_name="marketpriceindex",
            name="id",
        ),
        migrations.RemoveField(
            model_name="marketpriceindexpre2005",
            name="deleted",
        ),
        migrations.RemoveField(
            model_name="marketpriceindexpre2005",
            name="deleted_by_cascade",
        ),
        migrations.RemoveField(
            model_name="marketpriceindexpre2005",
            name="id",
        ),
        migrations.RemoveField(
            model_name="maxpriceindex",
            name="deleted",
        ),
        migrations.RemoveField(
            model_name="maxpriceindex",
            name="deleted_by_cascade",
        ),
        migrations.RemoveField(
            model_name="maxpriceindex",
            name="id",
        ),
        migrations.AlterField(
            model_name="constructionpriceindex",
            name="month",
            field=models.DateField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="constructionpriceindexpre2005",
            name="month",
            field=models.DateField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="marketpriceindex",
            name="month",
            field=models.DateField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="marketpriceindexpre2005",
            name="month",
            field=models.DateField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="maxpriceindex",
            name="month",
            field=models.DateField(primary_key=True, serialize=False),
        ),
    ]
