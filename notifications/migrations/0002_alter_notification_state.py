# Generated by Django 4.1.3 on 2023-07-03 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notifications", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="state",
            field=models.CharField(
                choices=[
                    ("read", "Read"),
                    ("unread", "Unread"),
                    ("deleted", "Deleted"),
                ],
                default="unread",
                max_length=20,
            ),
        ),
    ]
