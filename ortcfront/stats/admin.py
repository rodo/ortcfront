from django.contrib import admin
from .models import ViewAlertYear, AlertStats, ViewAlertUser
from .models import OsmUser
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class AlertUserResource(resources.ModelResource):

    class Meta:
        model = ViewAlertUser


class AlertYearResource(resources.ModelResource):

    class Meta:
        model = ViewAlertYear


class AlertMonthResource(resources.ModelResource):

    class Meta:
        model = ViewAlertYear


class ViewAlertYearAdmin(ImportExportModelAdmin):
    """Custom Admin for blocks
    """
    resource_class = AlertYearResource

    list_filter = ('year', 'alert_id')
    ordering = ['-year']

admin.site.register(ViewAlertYear, ViewAlertYearAdmin)
admin.site.register(OsmUser)
