from django.urls import path
from .views import DisplayAllRounds,DisplayUpdateDeleteRound
urlpatterns = [
    path("<int:communnity_id>/rounds/", DisplayAllRounds.as_view(),
         name="DisplayAllRounds"),
    path("round/<int:round_id>/",DisplayUpdateDeleteRound.as_view(),
         name="DisplayUpdateDeleteRound"),
]
