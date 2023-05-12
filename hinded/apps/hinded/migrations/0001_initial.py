# Generated by Django 4.2.1 on 2023-05-12 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hinded',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kirjeldus', models.CharField(max_length=500)),
                ('aine', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Isik',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eesnimi', models.CharField(max_length=100)),
                ('perenimi', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='IsikuHinne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vaartus', models.CharField(choices=[('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1'), ('X', 'X')], max_length=1)),
                ('markmed', models.CharField(max_length=100)),
                ('hinne', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hinded.hinded')),
                ('isik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hinded.isik')),
            ],
        ),
        migrations.AddConstraint(
            model_name='isikuhinne',
            constraint=models.UniqueConstraint(fields=('isik', 'hinne'), name='unikaalne_nimi_hinne'),
        ),
    ]