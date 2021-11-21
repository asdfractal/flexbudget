# Generated by Django 3.2.9 on 2021-11-21 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0003_alter_expenses_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='savings',
            name='annual_saving',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='savings',
            name='is_percent',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='savings',
            name='per_paycheck_saving',
            field=models.IntegerField(default=0),
        ),
    ]