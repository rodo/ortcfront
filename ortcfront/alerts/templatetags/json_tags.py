from django import template
from django.conf import settings

register = template.Library()

@register.filter
def get_key(dictionnary):
    return dictionnary.keys()[0]

@register.filter
def get_value(dictionnary):
    return dictionnary.values()[0]

@register.filter
def get_geom(dictionnary):
    print dictionnary
    return "k"
