from django.conf.urls import patterns, include, url

from rest_framework.authtoken import views

from django.contrib import admin
admin.autodiscover()

from userprofiles.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'StuffControl.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^entry/', 'userprofiles.views.entry', name='entry'),
    url(r'^logout/', 'userprofiles.views.logout_view', name='logout_view'),

    url(r'^thing/(\d+)', 'things.views.thing', name='thing'),
    url(r'^newthing/', 'things.views.new_thing', name='new_thing'),
    url(r'^create_newthing/', 'things.views.create_new_thing', name='create_new_thing'),
    url(r'^delete_thing/(\d+)', 'things.views.delete_thing', name='delete_thing'),
    url(r'^order_controller/', 'things.views.order_controller', name='order_controller'),
    url(r'^sensor_value/', 'things.views.sensor_value', name='sensor_value'),
    url(r'^add_automaticcontroller/', 'things.views.add_automaticcontroller', name='add_automaticcontroller'),
    url(r'^get_automaticcontroller/', 'things.views.get_automaticcontroller', name='get_automaticcontroller'),
    url(r'^change_check/(\d+)/(\d+)', 'things.views.change_check', name='change_check'),
    url(r'^delete_automatic/(\d+)', 'things.views.delete_automatic', name='delete_automatic'),
    url(r'^getthings/', 'things.views.getthings', name='getthings'),


    url(r'^newcamera/', 'cameras.views.new_camera', name='new_camera'),
    url(r'^create_newcamera/', 'cameras.views.create_new_camera', name='create_new_camera'),
    url(r'^camera/(\d+)', 'cameras.views.camera', name='camera'),
    url(r'^getcameras/', 'cameras.views.getcameras', name='getcameras'),

    url(r'^rest_login/', 'userprofiles.views.Rest_Login', name='rest_login'),
    url(r'^rest_get_things/', 'userprofiles.views.Rest_Get_Things', name='rest_get_things'),
    url(r'^rest_get_cameras/', 'userprofiles.views.Rest_Get_Cameras', name='rest_get_cameras'),
    url(r'^rest_get_thing_elements/(\d+)', 'userprofiles.views.Rest_Get_Thing_Elements', name='rest_get_thing_elements'),
    url(r'^rest_order_controller/', 'userprofiles.views.rest_order_controller', name='rest_order_controller'),

    url(r'^$', 'userprofiles.views.home', name='home'),



)

urlpatterns += [
    url(r'^api-token-auth/', views.obtain_auth_token)
]