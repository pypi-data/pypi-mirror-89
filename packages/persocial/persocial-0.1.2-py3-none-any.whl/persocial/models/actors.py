from django.db import models


class Actor(models.Model):
    class Meta:
        abstract = True


class Application(Actor):
    pass


class Group(Actor):
    pass


class Organization(Actor):
    pass


class Person(Actor):
    pass


class Service(Actor):
    pass
