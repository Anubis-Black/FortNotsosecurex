from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url('^', include('fort_notsosecurex.urls')),
    url(r'^admin/', include(admin.site.urls)),
)