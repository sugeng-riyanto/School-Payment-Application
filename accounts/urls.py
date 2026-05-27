from django.urls import path
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', lambda r: redirect('public_info:index'), name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/<int:pk>/edit/', views.edit_user, name='edit_user'),
    path('users/<int:pk>/delete/', views.delete_user, name='delete_user'),
    path('users/<int:pk>/reset-password/', views.reset_password, name='reset_password'),
    path('users/export/xlsx/', views.export_users_xlsx, name='export_users_xlsx'),
    path('import/students/', views.import_students, name='import_students'),
    path('download-template/<str:template_type>/', views.download_template, name='download_template'),
    path('grades/', views.grade_list, name='grade_list'),
    path('grades/create/', views.create_grade, name='create_grade'),
    path('grades/import/', views.import_grade, name='import_grade'),
    path('grades/<int:pk>/delete/', views.delete_grade, name='delete_grade'),
    path('class-grades/', views.class_grade_list, name='class_grade_list'),
    path('class-grades/create/', views.create_class_grade, name='create_class_grade'),
    path('class-grades/import/', views.import_class_grade, name='import_class_grade'),
    path('class-grades/<int:pk>/delete/', views.delete_class_grade, name='delete_class_grade'),
    path('grade-promotion/', views.grade_promotion, name='grade_promotion'),
    path('graduation/', views.graduation_list, name='graduation_list'),
    path('academic-years/', views.academic_year_list, name='academic_year_list'),
    path('academic-years/create/', views.academic_year_create, name='academic_year_create'),
    path('academic-years/<int:pk>/edit/', views.academic_year_edit, name='academic_year_edit'),
    path('academic-years/<int:pk>/delete/', views.academic_year_delete, name='academic_year_delete'),
    path('internal-info/', views.internal_info_list, name='internal_info_list'),
    path('internal-info/create/', views.internal_info_create, name='internal_info_create'),
    path('internal-info/<int:pk>/edit/', views.internal_info_edit, name='internal_info_edit'),
    path('internal-info/<int:pk>/delete/', views.internal_info_delete, name='internal_info_delete'),
    path('internal-info/<int:pk>/approve/', views.internal_info_approve, name='internal_info_approve'),
    path('personal-info/', views.personal_info_list, name='personal_info_list'),
    path('set-academic-year/', views.set_academic_year, name='set_academic_year'),
    path('blast-statistics/', views.blast_statistics, name='blast_statistics'),
]
