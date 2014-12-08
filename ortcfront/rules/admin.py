from django.contrib import admin
from .models import Rule, Domain
from import_export import resources
from import_export.admin import ImportExportModelAdmin

admin.site.register(Rule)
admin.site.register(Domain)

