# Generated by Django 3.2.9 on 2021-11-29 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20211124_1917'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='total_income',
            new_name='total_gross_salary',
        ),
        migrations.RenameField(
            model_name='customuser',
            old_name='total_expenses',
            new_name='total_paycheck_expenses',
        ),
        migrations.RenameField(
            model_name='customuser',
            old_name='total_savings',
            new_name='total_paycheck_savings',
        ),
        migrations.AddField(
            model_name='customuser',
            name='total_annual_expenses',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='customuser',
            name='total_annual_savings',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]