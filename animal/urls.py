from django.conf.urls import url

from . import views

app_name = 'animal'
urlpatterns = [
    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^dynamic-required-1$', views.DynamicRequired1.as_view(),
        name='dynamic_required_1'),
    url(r'^dynamic-required-2$', views.DynamicRequired2.as_view(),
        name='dynamic_required_2'),
]
