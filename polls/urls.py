from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('statics/', views.statics, name="statics"),
    
    path('ajax/load-cities/', views.load_restaurants, name='ajax_load_restaurants'), # AJAX
]
