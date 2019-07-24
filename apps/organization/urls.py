from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^(?P<org_id>\d+)$', views.org_info),
    url(r'^edit/(?P<org_id>\d+)$', views.edit),
    url(r'^new$', views.new),
    url(r'^create_org$', views.create_org),
    url(r'^remove/(?P<org_id>\d+)$', views.remove),
    url(r'^update/(?P<org_id>\d+)$', views.update_org),
    url(r'^cancel/(?P<joined_id>\d+)$', views.cancel_joined),
    url(r'^join/(?P<join_id>\d+)$', views.join_org),
]