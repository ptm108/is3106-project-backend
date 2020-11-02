# Generated by Django 3.1.2 on 2020-11-02 03:28

import datetime
from django.db import migrations, models
import django.db.models.manager
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Groupbuy',
            fields=[
                ('gb_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('current_order_quantity', models.PositiveIntegerField(default=0)),
                ('minimum_order_quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('approval_status', models.BooleanField(default=False)),
                ('order_by', models.DateTimeField()),
                ('final_price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('fulfillment_date', models.DateTimeField(default=datetime.datetime(2020, 11, 9, 3, 28, 38, 335016, tzinfo=utc))),
                ('delivery_fee', models.DecimalField(decimal_places=2, default=None, max_digits=6, null=True)),
            ],
            managers=[
                ('groupbuys', django.db.models.manager.Manager()),
            ],
        ),
    ]
