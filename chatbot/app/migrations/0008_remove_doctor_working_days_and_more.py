# Generated by Django 4.1.7 on 2023-04-23 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_appointment_end_time_appointment_start_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='working_days',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='working_hours_end',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='working_hours_start',
        ),
        migrations.CreateModel(
            name='WorkingDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='working_days', to='app.doctor')),
            ],
        ),
    ]