from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.EquipmentMain.as_view() , name='catalog_root'),
]