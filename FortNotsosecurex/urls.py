from django.conf.urls import patterns, include, url
from django.contrib import admin

from fort_notsosecurex import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login_user, name='login'),
    url(r'^register/', views.register_user, name='register'),
    url(r'^admin/', include(admin.site.urls)),
)