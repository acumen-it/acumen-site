# Generated by Django 2.2a1 on 2019-02-25 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acuthon', '0003_auto_20190224_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='team_lead',
            field=models.CharField(default=None, max_length=1024),
        ),
    ]
