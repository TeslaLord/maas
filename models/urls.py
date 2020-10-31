from django.urls import path
from . import views

urlpatterns = [
    path('', views.models, name='home'),
    path('sentiment/', views.sentiment, name='sentiment'),
    path('category/', views.category, name='category'),
    path('text_to_speech/', views.text_to_speech, name='text_to_speech'),
    path('speech_to_text/', views.speech_to_text, name='speech_to_text'),
    path('pdf/', views.pdf, name='pdf'),
]
