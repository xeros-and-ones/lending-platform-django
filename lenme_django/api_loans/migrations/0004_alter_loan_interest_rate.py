# Generated by Django 5.0 on 2023-12-28 06:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api_loans", "0003_alter_offer_interest_rate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loan",
            name="interest_rate",
            field=models.FloatField(default=15, null=True),
        ),
    ]