from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.redir, name="login"),
    path('login/', views.user_login, name="login"),
    path('login/', LogoutView.as_view(template_name="login.html"), name="logout"),
    
]
