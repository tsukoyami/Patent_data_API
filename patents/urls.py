from django.urls import path
from . import views

urlpatterns = [
    path('summary/', views.summary_view, name='summary'),
    path('query/', views.query_view, name='query'),
]