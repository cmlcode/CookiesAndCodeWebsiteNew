# Generated by Django 4.0.4 on 2022-08-20 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_customuser_membership_tier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='membership_tier',
            field=models.CharField(blank=True, choices=[('Platinum', 'Platinum'), ('Gold', 'Gold'), ('Silver', 'Silver'), ('Bronze', 'Bronze'), ('None', 'None')], default='N', max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='position',
            field=models.CharField(blank=True, choices=[('President', 'President'), ('Vice President', 'Vice President'), ('Vice President of Administration', 'Vice President of Administration'), ('Vice President of Finance', 'Vice President of Finance')], max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='year_in_school',
            field=models.CharField(blank=True, choices=[('Freshman', 'Freshman'), ('Sophomore', 'Sophomore'), ('Junior', 'Junior'), ('Senior', 'Senior'), ('Graduate', 'Graduate')], max_length=12, null=True),
        ),
    ]
