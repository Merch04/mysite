from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    
    path('', views.index, name="period"),
    path('statics/', views.statics, name="statics"),
    path('ajax/load-shifts/', views.load_shifts, name='ajax_load_shifts'), # AJAX
]
