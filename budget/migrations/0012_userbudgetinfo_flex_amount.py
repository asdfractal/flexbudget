# Generated by Django 3.2.9 on 2021-12-07 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0011_alter_expenses_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbudgetinfo',
            name='flex_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
