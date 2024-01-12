from django.urls import path
from . import views

urlpatterns = [
    path('<int:contest_id>/problems/<int:problem_id>/submit/', views.SubmitAnswerView.as_view()),
    path('<int:contest_id>/problems/', views.ContestProblemListView.as_view()),
    path('<int:contest_id>/problems/add/', views.AddProblemView.as_view()),
    path('', views.ContestListView.as_view()), 
    path('create/', views.CreateContestView.as_view()), 
    path('<int:contest_id>/problems/<int:pk>/', views.ProblemDetailView.as_view()),
    path('<int:contest_id>/end/', views.EndContestView.as_view()),
    path('problems', views.ProblemListView.as_view()),
]
