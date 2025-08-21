# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _


class AbstractName(models.Model):
    class Meta:
        abstract = True
        verbose_name = 'Nazwa'
        verbose_name_plural = 'Nazwy'

    name = models.CharField(
        max_length=256,
        verbose_name='Nazwa'
    )

    def __str__(self):
        return self.name


class RoomType(AbstractName):
    class Meta:
        verbose_name = 'Typ pokoju'
        verbose_name_plural = 'Typy pokojów'
        ordering = ('name',)


class Room(AbstractName):
    class Meta:
        verbose_name = 'Pokój'
        verbose_name_plural = 'Pokoje'
        ordering = ('name', )

    type = models.ForeignKey(
        'RoomType',
        verbose_name='Typ'
    )
    department = models.ForeignKey(
        'trainman.Department',
        verbose_name='Wydział'
    )

    def __str__(self):
        return '%s: %s' % (str(self.department), self.name)


class ItemType(AbstractName):
    class Meta:
        verbose_name = 'Typ przedmiotu'
        verbose_name_plural = 'Typy przedmiotów'
        ordering = ('name',)

    keys = models.ManyToManyField(
        'Key',
        blank=True,
        verbose_name='Klucz'
    )


class Item(AbstractName):
    class Meta:
        verbose_name = 'Przedmiot'
        verbose_name_plural = 'przedmioty'
        ordering = ('name', )

    serial_number = models.CharField(
        max_length=64,
        verbose_name='Numer seryjny'
    )
    inventory_number = models.CharField(
        max_length=64,
        verbose_name='Numer inwentarzowy'
    )
    invoice_number = models.CharField(
        max_length=64,
        verbose_name='Numer faktury'
    )
    price = models.FloatField(
        verbose_name='Cena (PLN):'
    )
    image = models.ImageField(
        upload_to='lock/img/',
        null=True,
        blank=True,
        verbose_name='Zdjęcie przedmiotu'
    )
    type = models.ForeignKey(
        'ItemType',
        verbose_name='Typ'
    )
    room = models.ForeignKey(
        'Room',
        verbose_name='Pokój'
    )
    item = models.ForeignKey(
        'Item',
        related_name='related_items',
        null=True,
        blank=True,
        verbose_name='Przedmiot'
    )
    users = models.ManyToManyField(
        'trainman.UserProfile',
        through='ItemUser',
        blank=True,
        verbose_name='Użytkownicy'
    )
    properties = models.ManyToManyField(
        'Key',
        through='Property',
        blank=True,
        verbose_name='Właściwości'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_(u'Zweryfikowany')
    )

    def __str__(self):
        return '%s, %s (%s)' % (str(self.type), self.name, self.serial_number)
    
    def get_item_owner(self):
        try:
            return self.users.filter(itemuser__type=ITEM_USER_TYPE_OWNER)[0]
        except IndexError:
            return ''
    
    def get_item_user(self):
        try:
            return self.users.filter(itemuser__type=ITEM_USER_TYPE_USER)[0]
        except IndexError:
            return ''


ITEM_USER_TYPE_OWNER = 1
ITEM_USER_TYPE_USER = 2


class ItemUserType(AbstractName):
    class Meta:
        verbose_name = 'Typ własności'
        verbose_name_plural = 'Typy własności'
        
    def __str__(self):
        return '%s' % self.name


class ItemUser(models.Model):
    class Meta:
        verbose_name = 'Użytkownik'
        verbose_name_plural = 'Użytkownicy'

    item = models.ForeignKey(
        'Item',
        verbose_name='Przedmiot'
    )
    user = models.ForeignKey(
        'trainman.UserProfile',
        verbose_name='Użytkownik'
    )
    type = models.ForeignKey(
        'ItemUserType',
        verbose_name='Typ'
    )
    date = models.DateField()

    def __str__(self):
        return '%s - %s, %s' % (str(self.item), str(self.user), str(self.type))


class Key(AbstractName):
    class Meta:
        verbose_name = 'Właściwość'
        verbose_name_plural = 'Właściwości'
        ordering = ('name', )


class Property(models.Model):
    class Meta:
        verbose_name = 'Właściwość przedmiotu'
        verbose_name_plural = 'Właściwości przedmiotów'

    value = models.CharField(
        max_length=1024,
        verbose_name='Wartość'
    )
    key = models.ForeignKey(
        'Key',
        verbose_name='Właściwość'
    )
    item = models.ForeignKey(
        'Item',
        verbose_name='Przedmiot'
    )

    def __stre__(self):
        return '%s, (%s: %s)' % (str(self.item), str(self.key), self.value)


class LockAdmin(models.Model):
    class Meta:
        verbose_name = 'Administrator Locka'
        verbose_name_plural = 'Administratorzy Locka'

    user_profile = models.OneToOneField(
        'trainman.UserProfile',
        verbose_name='Użytkownik'
    )
    departments = models.ManyToManyField(
        'trainman.Department',
        blank=True,
        verbose_name='Administrowane jednostki'
    )

    def __str__(self):
        return str(self.user_profile)
