# Generated by Django 3.1 on 2020-08-28 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messagebot', '0005_auto_20200828_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='event_id',
            field=models.CharField(max_length=16, primary_key=True, serialize=False),
        ),
    ]