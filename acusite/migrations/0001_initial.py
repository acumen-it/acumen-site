# Generated by Django 2.1.3 on 2019-03-07 15:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.CharField(default='NULL', max_length=5, primary_key=True, serialize=False)),
                ('event_name', models.CharField(max_length=50)),
                ('team_size', models.IntegerField(default=1)),
                ('event_cost', models.IntegerField(default=0)),
                ('participation_points', models.IntegerField(default=0)),
                ('merit_points', models.IntegerField(default=0)),
                ('event_organiser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_choice', models.CharField(choices=[('R', 'RUNNING'), ('P', 'PLAYED'), ('W', 'WAITING')], default='WAITING', max_length=8)),
                ('team_id', models.CharField(max_length=20)),
                ('amount_paid', models.BooleanField(default=False)),
                ('payment_mode', models.CharField(choices=[('R', 'RUNNING'), ('P', 'PLAYED'), ('W', 'WAITING')], default='OFF', max_length=10)),
                ('event_id', models.ForeignKey(max_length=5, on_delete='CASCADE', to='acusite.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Otpgenerator',
            fields=[
                ('mailid', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('otp', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=32)),
                ('payment_status', models.CharField(max_length=30)),
                ('payment_request_id', models.CharField(max_length=32)),
                ('eventname', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_number', models.CharField(default='1602-70-700-777', max_length=20)),
                ('year', models.CharField(choices=[('I', 'I'), ('II', 'II'), ('III', 'III'), ('IV', 'IV')], default='I', max_length=2)),
                ('branch', models.CharField(choices=[('IT', 'INFORMATION TECHNOLOGY'), ('EEE', 'ELECTRICAL AND ELECTRONICS ENGINEERING'), ('ECE', 'ELECTRONICS AND COMMUNICATION ENGINEERING'), ('CIVIL', 'CIVIL'), ('CSE', 'COMPUTER SCIENCE'), ('MECH', 'MECHANICAL'), ('CHEMICAL', 'CHEMICAL'), ('EIE', 'ELECTRONICS AND INSTRUMENTATION ENGINEERING'), ('TEXTILE', 'TEXTILE')], default='IT', max_length=50)),
                ('college', models.CharField(max_length=50)),
                ('phone_number', models.CharField(default='NoNumber', max_length=10)),
                ('qr_code', models.CharField(default=0, max_length=30)),
                ('total_points', models.IntegerField(default=0)),
                ('cost', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_id', models.CharField(max_length=20, unique=True)),
                ('team_size', models.IntegerField(default=1)),
                ('event_id', models.ForeignKey(max_length=5, on_delete='CASCADE', to='acusite.Event')),
            ],
        ),
        migrations.AddField(
            model_name='eventdetails',
            name='qr_code',
            field=models.ForeignKey(max_length=50, on_delete='CASCADE', to='acusite.Profile'),
        ),
    ]
