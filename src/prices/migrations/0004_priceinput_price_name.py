# Generated by Django 2.2.5 on 2020-01-04 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prices', '0003_auto_20200102_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='priceinput',
            name='price_name',
            field=models.CharField(db_column='priceName', default='Price Model 1', max_length=45),
            preserve_default=False,
        ),
    ]
