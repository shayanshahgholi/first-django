from django.urls import path
from . import views

urlpatterns = [
    path ('main', views.main_page, name = 'index'),
    path ('<int:question_id>/', views.detail, name='detail'),
    path ('result/<int:question_id>', views.result, name = 'result'),
    path ('vote/<int:question_id>', views.vote, name='vote'),
    path ('add_vote/<int:question_id>', views.add_vote, name='add_vote')
]
