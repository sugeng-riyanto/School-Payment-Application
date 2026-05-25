from django.urls import path
from . import views

app_name = 'calendars'

urlpatterns = [
    path('', views.calendar_list, name='list'),
    path('upload/', views.upload_calendar, name='upload'),
    path('<int:pk>/edit/', views.edit_calendar, name='edit'),
]
