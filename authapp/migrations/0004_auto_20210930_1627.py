# Generated by Django 2.2.17 on 2021-09-30 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'М'), ('W', 'Ж')], max_length=1, verbose_name='пол'),
        ),
    ]