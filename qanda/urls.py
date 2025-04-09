from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='qanda/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='qanda/logout.html'), name='logout'),
    path('question/new/', views.post_question, name='post-question'),
    path('question/<int:pk>/', views.QuestionDetailView.as_view(
    ), name='question-detail'),
    path('question/<int:question_id>/answer/', views.post_answer,
         name='post-answer'),
    path('like/', views.like_answer, name='like-answer'),
]
