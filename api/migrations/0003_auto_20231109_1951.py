# Generated by Django 3.2.14 on 2023-11-09 10:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20231109_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='review_count',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(default=1, help_text='1から5の範囲で評価をつけてください。', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
