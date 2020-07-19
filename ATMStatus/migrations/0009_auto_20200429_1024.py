# Generated by Django 3.0.4 on 2020-04-29 04:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ATMStatus', '0008_auto_20200429_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atmdetails',
            name='branch_code',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='atmdetails',
            name='branch_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ATMStatus.BranchDetails'),
        ),
        migrations.AlterField(
            model_name='atmissuedetails',
            name='branch_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AtmDetails_branch_name', to='ATMStatus.BranchDetails'),
        ),
    ]