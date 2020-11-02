# Generated by Django 3.1.2 on 2020-11-02 03:28

from django.db import migrations, models
import django.db.models.manager
import django.utils.timezone
import recipes.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('ing_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('foreign_id', models.CharField(editable=False, max_length=50)),
                ('ing_name', models.CharField(max_length=200)),
                ('image_url', models.URLField(max_length=300)),
                ('category', models.CharField(max_length=100)),
                ('quantity', models.CharField(default='', max_length=100)),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('estimated_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('metadata', models.JSONField()),
            ],
            managers=[
                ('ingredient_list', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('recipe_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('recipe_name', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('estimated_price_start', models.DecimalField(decimal_places=2, max_digits=6)),
                ('estimated_price_end', models.DecimalField(decimal_places=2, max_digits=6)),
                ('deleted', models.BooleanField(default=False)),
                ('display_photo', models.ImageField(blank=True, default='', null=True, upload_to=recipes.models.recipe_directory_path)),
            ],
            managers=[
                ('recipe_book', django.db.models.manager.Manager()),
            ],
        ),
    ]
