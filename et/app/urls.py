from django.urls import path , include
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.login,name="login"),
    path('add/', views.add,name="add"),
    path('base/', views.base,name="base"),
    path('home/', views.home,name="home"),
    path('display/', views.display,name="display"),
    path('edit/', views.edit,name="edit"),
    path('homepage/', views.homepage,name="homepage"),
    path('limit/', views.limit,name="limit"),
    path('signup/', views.signup,name="signup"),
    path('month/', views.month,name="month"),
    path('logout/', LogoutView.as_view(), name='logout'),
]