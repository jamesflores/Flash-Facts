from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:month>/<int:day>/', views.index, name='index'),
    path('about', views.about, name='about'),
]