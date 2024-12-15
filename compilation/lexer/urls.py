# compilation/lexer/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('compile/', views.CompileView.as_view(), name='compile'),
]