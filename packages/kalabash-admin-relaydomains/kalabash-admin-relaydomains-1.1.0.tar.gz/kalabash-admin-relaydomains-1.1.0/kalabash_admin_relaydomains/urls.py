from django.conf.urls import patterns, url

urlpatterns = patterns(
    'kalabash_admin_relaydomains.views',

    url(r'^relaydomains/scan_services/$', 'scan_for_services',
        name="service_scan"),
)
