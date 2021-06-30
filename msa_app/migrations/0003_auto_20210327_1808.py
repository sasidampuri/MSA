# Generated by Django 3.1.7 on 2021-03-27 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msa_app', '0002_auto_20210327_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='confirm_password',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='middle_name',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='generic_name',
            field=models.CharField(default='default generic name', max_length=50),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='trade_name',
            field=models.CharField(default='default trade name', max_length=50),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='unit_purchase_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='unit_sell_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='medicinetovendor',
            name='medicine_id',
            field=models.CharField(default='MED', max_length=10),
        ),
        migrations.AlterField(
            model_name='medicinetovendor',
            name='vendor_id',
            field=models.CharField(default='VEN', max_length=10),
        ),
        migrations.AlterField(
            model_name='stock',
            name='batch_id',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='expiry_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='medicine_id',
            field=models.CharField(default='MED', max_length=10),
        ),
        migrations.AlterField(
            model_name='stock',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='address',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='medicine_ids',
            field=models.CharField(default='MED', max_length=100),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='mobile',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='vendor_name',
            field=models.CharField(default='default vendor', max_length=50),
        ),
    ]
