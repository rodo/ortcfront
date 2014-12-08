from django.contrib import admin
from .models import ViewAlertYear, AlertStats, ViewAlertUser
from .models import AlertUserStats
from .models import OsmUser
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class AlertUserResource(resources.ModelResource):

    class Meta:
        fields = ('alert_id', 'date_stat',
                  'year', 'month',
                  'userid', 'username', 'item',
                  'created', 'modified', 'deleted')
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
    readonly_fields = ('year', 'alert_id','created','deleted','modified')
    list_filter = ('year', 'alert_id')
    list_display = ('year', 'alert_id', 'created', 'deleted', 'modified')
    ordering = ['-year']

admin.site.register(AlertUserStats)
admin.site.register(ViewAlertYear, ViewAlertYearAdmin)
admin.site.register(OsmUser)
