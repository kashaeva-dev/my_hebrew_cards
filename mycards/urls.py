from django.urls import path

import mycards.views as views

urlpatterns = [
    path('', views.cards_main, name='main'),
    path('verbs_print/', views.cards_verbs, name='verbs_print'),
    path('nouns_exceptions/', views.table_nouns_exceptions, name='nouns_exceptions'),
    path('questions/', views.question_words, name='questions'),
    path('adjectives/', views.adjectives, name='adjectives'),
    path('nouns/', views.nouns_all, name='nouns'),
    path('nouns/<str:cats_ids>/', views.nouns_filter, name='nouns_filter'),
    path('verbs/', views.verbs_all, name='verbs'),
    path('verbs/<str:cats_ids>/', views.verbs_filter, name='verbs_filter'),
    path('numbers/', views.numbers, name='numbers'),
    path('pronouns/', views.pronouns, name='pronouns'),
]