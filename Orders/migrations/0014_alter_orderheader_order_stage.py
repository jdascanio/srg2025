# Generated by Django 4.1.1 on 2025-02-13 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0013_alter_order_order_nr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderheader',
            name='order_stage',
            field=models.CharField(default='noenvio', max_length=60),
        ),
    ]
