# Generated by Django 4.1.1 on 2025-02-01 02:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0003_ordercontent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordercontent',
            name='order_number',
        ),
        migrations.RemoveField(
            model_name='ordercontent',
            name='user',
        ),
        migrations.RemoveField(
            model_name='orderheader',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderheader',
            name='user',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderContent',
        ),
        migrations.DeleteModel(
            name='OrderHeader',
        ),
    ]
