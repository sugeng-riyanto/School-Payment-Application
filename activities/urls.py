from django.urls import path
from . import views

app_name = 'activities'

urlpatterns = [
    path('', views.activity_list, name='list'),
    path('create/', views.create_activity, name='create'),
    path('<slug:slug>/', views.activity_detail, name='detail'),
    path('<slug:slug>/edit/', views.edit_activity, name='edit'),
    path('<slug:slug>/publish/', views.publish_activity, name='publish'),
    path('<slug:slug>/review/', views.review_activity, name='review'),
    path('<slug:slug>/pic-review/', views.pic_review_activity, name='pic_review'),
    path('types/', views.activity_type_list, name='type_list'),
    path('types/create/', views.create_activity_type, name='create_type'),
    path('types/<int:pk>/edit/', views.edit_activity_type, name='edit_type'),
    path('types/<int:pk>/delete/', views.delete_activity_type, name='delete_type'),
    path('types/import/', views.import_activity_types, name='import_types'),
    path('types/download-template/', views.download_type_template, name='download_type_template'),
]
