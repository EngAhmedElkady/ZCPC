from django.urls import path, include
from . import views


urlpatterns = [
    # Level
    path('in_round/<int:round_id>/', views.GetLevelAndCreate.as_view()),
    path('level_details/<int:pk>', views.GetLevelAndUpdateAndDelete.as_view()),

    # team
    path('team/<int:level_id>/', views.GetLevelTeamAndCreate.as_view()),
    path('team/member/<int:pk>/', views.GetLevelTeamAndUpdateAndDelete.as_view()),

    # student
    path("students/<int:level_id>/", views.GetLevelStudentAndCreate.as_view()),
    path("students/student_details/<int:pk>/",
         views.GetLevelstudentAndUpdateAndDelete.as_view()),

    # feedback
    path("feedback/<int:level_id>/", views.GetLevelFeedbackAndCreate.as_view()),
    path("feedback/feedback_details/<int:pk>/",
         views.GetLevelfeedbacktAndUpdateAndDelete.as_view()),

    # feedback
    path("teamfeedback/<int:level_id>/",
         views.GetTeamFeedbackAndCreate.as_view()),
    path("teamfeedback/teamfeedback_details/<int:pk>/",
         views.GetTeamfeedbacktAndUpdateAndDelete.as_view()),

]
