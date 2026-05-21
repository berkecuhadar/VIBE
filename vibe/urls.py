from django.urls import path
from . import views

urlpatterns = [
    # Main Portal and Dynamic Ranking Board
    path('', views.home_page, name='home_page'),
    
    # Knowledge Base & Bi-Directional Voting Mechanics
    path('codex/', views.codex_page, name='codex_page'),
    path('vote/<int:character_id>/<str:vote_type>/', views.cast_vote, name='cast_vote'),
    
    # Community Contribution Proposals
    path('suggest-character/', views.suggest_character, name='suggest_character'),
    path('suggest-codex/', views.suggest_codex, name='suggest_codex'),
]