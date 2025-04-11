# Generated by Django 5.0.1 on 2025-04-10 20:27

import django.contrib.gis.db.models.fields
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('emoji', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Kategoriya',
                'verbose_name_plural': 'Kategoriyalar',
            },
        ),
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(unique=True, verbose_name='Foydalanuvchi ID')),
                ('username', models.CharField(blank=True, max_length=255, null=True, verbose_name='Username')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ism')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Familiya')),
                ('total_searches', models.IntegerField(default=0, verbose_name='Qidiruvlar soni')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faol')),
                ('last_seen', models.DateTimeField(auto_now=True, verbose_name='Oxirgi faollik')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name="Ro'yxatdan o'tgan sana")),
            ],
            options={
                'verbose_name': 'Foydalanuvchi',
                'verbose_name_plural': 'Foydalanuvchilar',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nomi')),
                ('address', models.TextField(verbose_name='Manzil')),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='Joylashuv')),
                ('working_hours', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ish vaqti')),
                ('contact', models.CharField(blank=True, max_length=255, null=True, verbose_name='Kontakt')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faol')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Yaratilgan vaqt')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.category', verbose_name='Kategoriya')),
            ],
            options={
                'verbose_name': 'Lokatsiya',
                'verbose_name_plural': 'Lokatsiyalar',
            },
        ),
        migrations.CreateModel(
            name='UserSearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(verbose_name='Foydalanuvchi ID')),
                ('latitude', models.FloatField(verbose_name='Kenglik')),
                ('longitude', models.FloatField(verbose_name='Uzunlik')),
                ('results_count', models.IntegerField(default=0, verbose_name='Natijalar soni')),
                ('search_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Qidiruv vaqti')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.category', verbose_name='Kategoriya')),
            ],
            options={
                'verbose_name': 'Qidiruv',
                'verbose_name_plural': 'Qidiruvlar',
            },
        ),
    ]
