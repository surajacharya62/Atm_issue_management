# Generated by Django 3.0.4 on 2020-04-29 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ATMStatus', '0006_auto_20200428_1747'),
    ]

    operations = [
        migrations.CreateModel(
            name='BranchDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_n', models.IntegerField()),
                ('branch_name', models.CharField(max_length=100)),
                ('branch_code', models.IntegerField()),
            ],
        ),
    ]