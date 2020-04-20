# Generated by Django 3.0.5 on 2020-04-16 08:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stocks.Company'),
        ),
        migrations.AddField(
            model_name='stock',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='stock',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
