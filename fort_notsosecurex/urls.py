from django.conf.urls import patterns, url
from fort_notsosecurex import views

urlpatterns = patterns(
    '',
    # /
    url(r'^$', views.index, name='index'),
    # /1000567
    url(r'^(?P<account_id>[1-9][0-9]{6})/$', views.get_account, name='account'),
    # /login/
    url(r'^login/', views.login_user, name='login'),
    # /logout/
    url(r'^logout/', views.logout_user, name='logout'),
    # /register/
    url(r'^register/', views.register_user, name='register'),
    # /transfer/
    url(r'^transfer/', views.make_transfer, name='transfer'),
)