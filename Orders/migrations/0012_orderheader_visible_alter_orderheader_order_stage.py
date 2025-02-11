# Generated by Django 4.1.1 on 2025-02-10 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0011_orderheader_ordercontent'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderheader',
            name='visible',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='orderheader',
            name='order_stage',
            field=models.CharField(default='envio', max_length=60),
        ),
    ]
