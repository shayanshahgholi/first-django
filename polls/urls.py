from django.urls import path
from . import views

urlpatterns = [
    path ('main', views.MainPage.as_view(), name = 'index'),
    path ('<int:pk>/', views.Detail.as_view(), name='detail'),
    path ('result/<int:pk>', views.Result.as_view(), name = 'result'),
    path ('vote/<int:question_id>', views.vote, name='vote'),
    path ('add_vote/<int:question_id>', views.add_vote, name='add_vote')
]
