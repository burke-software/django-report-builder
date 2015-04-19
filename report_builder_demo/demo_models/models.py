from django.db import models
from custom_field.custom_field import CustomFieldModel


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

    @property
    def i_want_char_field(self):
        return 'lol no'

    class ReportBuilder:
        extra = ('i_want_char_field',)


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

    def __str__(self):
        return "%s the waiter at %s" % (self.name, self.restaurant)
