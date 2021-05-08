from django.urls import path
from .views import input_user, recommendations

urlpatterns = [
    path('', input_user),
    path('recommendations/', recommendations)
]