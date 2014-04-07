from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^rules/', include('ortcfront.rules.urls')),
                       url(r'^alerts/', include('ortcfront.alerts.urls')),
                       url(r'^$', 'ortcfront.users.views.home', name='home'),

                       url(r'^accounts/', include('registration.backends.default.urls')),
    # url(r'^ortcfront/', include('ortcfront.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

)
