from django.db import models
from django.utils.functional import cached_property
from custom_field.custom_field import CustomFieldModel

from djmoney.models.fields import MoneyField


class Foo(models.Model):
    char_field = models.CharField(max_length=50, blank=True)
    char_field2 = models.CharField(max_length=50, blank=True)

    class ReportBuilder:
        fields = ('char_field',)


class FooExclude(Foo):
    class ReportBuilder:
        exclude = ('char_field2',)


class Bar(CustomFieldModel, models.Model):
    char_field = models.CharField(max_length=50, blank=True)
    foos = models.ManyToManyField(Foo, blank=True)

    CHECK = 'CH'
    MATE = 'MA'
    CHESS_CHOICES = (
        (CHECK, 'CHECK'),
        (MATE, 'CHECKMATE'),
    )

    check_mate_status = models.CharField(
        max_length=2,
        choices=CHESS_CHOICES,
        default=CHECK
    )

    @property
    def i_want_char_field(self):
        return 'lol no'

    @cached_property
    def i_need_char_field(self):
        return 'lol yes'

    class ReportBuilder:
        extra = ('i_want_char_field', 'i_need_char_field',)
        filters = ('char_field',)


class Account(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    balance = MoneyField(max_digits=10, decimal_places=2, default_currency='USD', blank=True, null=True)
    budget = MoneyField(max_digits=20, decimal_places=4, default_currency='USD', blank=True, null=True)

    class ReportBuilder:
        fields = ('budget', 'id', 'name', 'balance',)
        filters = ('budget',)
        defaults = ('budget',)
        exclude = ('balance_currency',)


class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

    def __str__(self):
        return "%s the place" % self.name


class Restaurant(models.Model):
    place = models.OneToOneField(Place, primary_key=True)
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    def __str__(self):
        return "%s the restaurant" % self.place.name


class Waiter(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    name = models.CharField(max_length=50)
    days_worked = models.IntegerField(blank=True, null=True, default=None)

    def __str__(self):
        return "%s the waiter at %s" % (self.name, self.restaurant)


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class Child(models.Model):
    parent = models.ForeignKey(Person, related_name='children')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(null=True, blank=True, default=None)
    color = models.CharField(max_length=1, blank=True, default='', choices=(
        ('R', 'Red'),
        ('G', 'Green'),
        ('B', 'Blue'),
    ))
