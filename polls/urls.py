from django.urls import path
from . import views

urlpatterns = [
    path ('main', views.main_page, name = 'index'),
    path ('<int:question_id>/', views.detail, name='detail'),
]
