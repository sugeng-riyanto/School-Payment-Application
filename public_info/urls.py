from django.urls import path
from . import views

app_name = 'public_info'

urlpatterns = [
    # Public pages (no login)
    path('', views.public_index, name='index'),
    path('profil/', views.school_profile, name='school_profile'),
    path('kurikulum/', views.curriculum_info, name='curriculum'),
    path('guru/', views.teacher_list, name='teachers'),
    path('penilaian/', views.grading_info, name='grading'),
    path('kalender/', views.public_calendar, name='calendar'),
    path('verify/', views.public_verify_invoice, name='verify_invoice'),

    # Admin CRUD
    path('admin/profil/', views.admin_school_profile, name='admin_school_profile'),
    path('admin/kontak/', views.admin_contacts, name='admin_contacts'),
    path('admin/sosial/', views.admin_social, name='admin_social'),
    path('admin/kurikulum/', views.admin_curriculum, name='admin_curriculum'),
    path('admin/program/', views.admin_programs, name='admin_programs'),
    path('admin/guru/', views.admin_teachers, name='admin_teachers'),
    path('admin/guru/<int:pk>/edit/', views.admin_teachers, name='admin_teachers_edit'),
    path('admin/penilaian/', views.admin_grading, name='admin_grading'),
    path('admin/guru/template/', views.download_teacher_template_xlsx, name='download_teacher_template'),
    path('admin/guru/import/', views.import_teachers_xlsx, name='import_teachers'),
    path('admin/guru/structure/', views.admin_teacher_structure, name='admin_teacher_structure'),
    path('demo/', views.demo_selection, name='demo_login'),
    path('lang/', views.set_language, name='set_language'),
]
