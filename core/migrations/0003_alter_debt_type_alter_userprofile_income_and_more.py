# Generated by Django 5.2.4 on 2025-07-06 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_expense_description_debt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debt',
            name='type',
            field=models.CharField(choices=[('loan', 'Loan'), ('emi', 'EMI'), ('credit_card', 'Credit Card'), ('other', 'Other')], max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='income',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='savings',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
