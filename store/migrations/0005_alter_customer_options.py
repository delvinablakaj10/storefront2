# Generated by Django 5.1a1 on 2024-06-20 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0004_alter_order_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customer",
            options={
                "ordering": ["user__first_name", "user__last_name"],
                "permissions": [("view_history", "Can view history")],
            },
        ),
    ]
