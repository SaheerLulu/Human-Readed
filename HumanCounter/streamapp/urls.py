from django.urls import path
from .views import live_count

urlpatterns = [
    path('live-count/', live_count, name='live_count'),
]