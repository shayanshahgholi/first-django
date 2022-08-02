from django.urls import path
from . import views

urlpatterns = [
    path ('main', views.MainPage.as_view(), name = 'index'),
    path ('<int:pk>/', views.Detail.as_view(), name='detail'),
    path ('result/<int:pk>', views.Result.as_view(), name = 'result'),
    path ('vote/<int:question_id>', views.vote, name='vote'),
    path ('add_vote/<int:question_id>', views.add_vote, name='add_vote'),
    path ('login', views.login_page, name='login'),
    path ('login_user', views.login_user, name='login_user'),
    path ('logout', views.logout_page, name='logout'),
    path ('register', views.register_page, name='register_page'),
    path ('register_add', views.register, name='register')
]
