from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def osm_item(id_type):
    return settings.OSM_ITEMS[str(id_type)]

@register.simple_tag
def osm_www():
    return settings.OSM_WWW
