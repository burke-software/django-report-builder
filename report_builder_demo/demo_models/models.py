from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.functional import cached_property

from djmoney.models.fields import MoneyField


class Foo(models.Model):
    char_field = models.CharField(max_length=50, blank=True)
    char_field2 = models.CharField(max_length=50, blank=True)

    class ReportBuilder:
        fields = ('char_field',)


class FooExclude(Foo):
    class ReportBuilder:
        exclude = ('char_field2',)


class Bar(models.Model):
    char_field = models.CharField(max_length=50, blank=True)
    foos = models.ManyToManyField(Foo, blank=True, related_name='bar_set')

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
    place = models.OneToOneField(Place, primary_key=True, on_delete=models.CASCADE)
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    def __str__(self):
        return "%s the restaurant" % self.place.name


class Waiter(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    days_worked = models.IntegerField(blank=True, null=True, default=None)

    def __str__(self):
        return "%s the waiter at %s" % (self.name, self.restaurant)


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    last_login = models.DateField(
        auto_now=True)
    last_modifed = models.DateField(
        null=True,
        blank=True)
    birth_date = models.DateTimeField(
        null=True,
        blank=True)
    hammer_time = models.TimeField(
        null=True,
        blank=True,
        help_text="U Can't Touch This")


class Child(models.Model):
    parent = models.ForeignKey(Person, related_name='children', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(null=True, blank=True, default=None)
    color = models.CharField(max_length=1, blank=True, default='', choices=(
        ('R', 'Red'),
        ('G', 'Green'),
        ('B', 'Blue'),
    ))


class Comment(models.Model):
    """ django-contrib-comments like model """
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
    object_pk = models.TextField()
    content_object = GenericForeignKey(
        ct_field="content_type", fk_field="object_pk")
