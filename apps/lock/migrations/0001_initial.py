# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainman', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=256, verbose_name='Nazwa')),
                ('serial_number', models.CharField(max_length=64, verbose_name='Numer seryjny')),
                ('inventory_number', models.CharField(max_length=64, verbose_name='Numer inwentarzowy')),
                ('invoice_number', models.CharField(max_length=64, verbose_name='Numer faktury')),
                ('price', models.FloatField(verbose_name='Cena (PLN):')),
                ('image', models.ImageField(null=True, upload_to='lock/img/', blank=True, verbose_name='Zdjęcie przedmiotu')),
                ('is_verified', models.BooleanField(default=False, verbose_name='Zweryfikowany')),
                ('item', models.ForeignKey(null=True, to='lock.Item', blank=True, verbose_name='Przedmiot', related_name='related_items')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Przedmiot',
                'verbose_name_plural': 'przedmioty',
            },
        ),
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=256, verbose_name='Nazwa')),
            ],
            options={
                'verbose_name': 'Typ przedmiotu',
                'verbose_name_plural': 'Typy przedmiotów',
            },
        ),
        migrations.CreateModel(
            name='ItemUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('date', models.DateField()),
                ('item', models.ForeignKey(verbose_name='Przedmiot', to='lock.Item')),
            ],
            options={
                'verbose_name': 'Użytkownik',
                'verbose_name_plural': 'Użytkownicy',
            },
        ),
        migrations.CreateModel(
            name='ItemUserType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=256, verbose_name='Nazwa')),
            ],
            options={
                'verbose_name': 'Typ własności',
                'verbose_name_plural': 'Typy własności',
            },
        ),
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=256, verbose_name='Nazwa')),
            ],
            options={
                'verbose_name': 'Właściwość',
                'verbose_name_plural': 'Właściwości',
            },
        ),
        migrations.CreateModel(
            name='LockAdmin',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('departments', models.ManyToManyField(to='trainman.Department', blank=True, verbose_name='Administrowane jednostki')),
                ('user_profile', models.OneToOneField(to='trainman.UserProfile', verbose_name='Użytkownik')),
            ],
            options={
                'verbose_name': 'Administrator Locka',
                'verbose_name_plural': 'Administratorzy Locka',
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('value', models.CharField(max_length=1024, verbose_name='Wartość')),
                ('item', models.ForeignKey(verbose_name='Przedmiot', to='lock.Item')),
                ('key', models.ForeignKey(verbose_name='Właściwość', to='lock.Key')),
            ],
            options={
                'verbose_name': 'Właściwość przedmiotu',
                'verbose_name_plural': 'Właściwości przedmiotów',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=256, verbose_name='Nazwa')),
                ('department', models.ForeignKey(verbose_name='Wydział', to='trainman.Department')),
            ],
            options={
                'verbose_name': 'Pokój',
                'verbose_name_plural': 'Pokoje',
            },
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=256, verbose_name='Nazwa')),
            ],
            options={
                'verbose_name': 'Typ pokoju',
                'verbose_name_plural': 'Typy pokojów',
            },
        ),
        migrations.AddField(
            model_name='room',
            name='type',
            field=models.ForeignKey(verbose_name='Typ', to='lock.RoomType'),
        ),
        migrations.AddField(
            model_name='itemuser',
            name='type',
            field=models.ForeignKey(verbose_name='Typ', to='lock.ItemUserType'),
        ),
        migrations.AddField(
            model_name='itemuser',
            name='user',
            field=models.ForeignKey(verbose_name='Użytkownik', to='trainman.UserProfile'),
        ),
        migrations.AddField(
            model_name='itemtype',
            name='keys',
            field=models.ManyToManyField(to='lock.Key', blank=True, verbose_name='Klucz'),
        ),
        migrations.AddField(
            model_name='item',
            name='properties',
            field=models.ManyToManyField(to='lock.Key', through='lock.Property', blank=True, verbose_name='Właściwości'),
        ),
        migrations.AddField(
            model_name='item',
            name='room',
            field=models.ForeignKey(verbose_name='Pokój', to='lock.Room'),
        ),
        migrations.AddField(
            model_name='item',
            name='type',
            field=models.ForeignKey(verbose_name='Typ', to='lock.ItemType'),
        ),
        migrations.AddField(
            model_name='item',
            name='users',
            field=models.ManyToManyField(to='trainman.UserProfile', through='lock.ItemUser', blank=True, verbose_name='Użytkownicy'),
        ),
    ]
