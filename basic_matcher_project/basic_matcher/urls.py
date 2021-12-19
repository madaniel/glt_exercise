from django.urls import path
from basic_matcher.views import CandidateView, CandidateMatchView, JobView, SkillView

app_name = "basic_matcher"


urlpatterns = [
    path('skills/', SkillView.as_view()),
    path('skills/<int:pk>', SkillView.as_view()),
    path('jobs/', JobView.as_view()),
    path('jobs/<int:pk>', JobView.as_view()),
    path('candidates/', CandidateView.as_view()),
    path('candidates/<int:pk>', CandidateView.as_view()),
    path('match/', CandidateMatchView.as_view()),
    path('match/<int:pk>', CandidateMatchView.as_view()),
    ]
