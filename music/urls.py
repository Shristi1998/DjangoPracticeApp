from django.urls import path
from . import views;
app_name='music'
urlpatterns = [
    path('', views.index, name='index'),
    path('<album_id>', views.detail, name='detail'),
    path('<album_id>/favourite', views.favourite, name='favourite'),
]