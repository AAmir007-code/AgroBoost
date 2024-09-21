from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('map/<int:z>/<int:x>/<int:y>', views.loadMap, name='index'),
    path('getLoadByXYZ', views.getLoadByXYZ, name='index'),
    path('loadByXYZ', views.loadByXYZ, name='index'),
    path('loadAllByXYZ', views.loadAllByXYZ, name='index'),
]
