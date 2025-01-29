# Generated by Django 4.1.1 on 2025-01-29 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subcat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcat', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='products',
            name='subcat',
            field=models.CharField(default='null', max_length=20),
            preserve_default=False,
        ),
    ]
