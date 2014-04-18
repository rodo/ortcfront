from django import template
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry

register = template.Library()

@register.filter
def coord_from_wkt(wkt):
    pnt = GEOSGeometry(wkt)
    return ",".join([str(coord) for coord in pnt])
