# Generated by Django 5.1.4 on 2024-12-17 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_alter_order_options_order_is_pending"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="is_pending",
            field=models.BooleanField(default=False, verbose_name="В ожидании"),
        ),
    ]
