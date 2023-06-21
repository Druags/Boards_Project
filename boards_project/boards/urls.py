from django.urls import path

from . import views

urlpatterns = [
    path('api/boards/', views.BoardViewAPI.as_view()),
]