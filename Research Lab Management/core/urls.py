
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('export-report/', views.export_report, name='export_report'),
]
