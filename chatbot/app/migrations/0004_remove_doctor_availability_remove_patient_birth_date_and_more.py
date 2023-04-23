# Generated by Django 4.1.7 on 2023-04-22 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_first_name_patient_full_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='availability',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='birth_date',
        ),
        migrations.AddField(
            model_name='doctor',
            name='about',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='working_days',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='patient',
            name='allergies',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='medications',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.patient')),
            ],
        ),
    ]