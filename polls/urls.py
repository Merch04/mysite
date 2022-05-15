from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('statics/', views.statics, name="statics"),
    
    path('ajax/load-shifts/', views.load_shifts, name='ajax_load_shifts'), # AJAX
]
