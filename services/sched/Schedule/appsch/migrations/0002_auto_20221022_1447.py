# Generated by Django 2.2.28 on 2022-10-22 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appsch', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
