from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('export/spp/xlsx/', views.export_spp_xlsx, name='export_spp_xlsx'),
    path('export/spp/pdf/', views.export_spp_pdf, name='export_spp_pdf'),
    path('export/eca/xlsx/', views.export_eca_xlsx, name='export_eca_xlsx'),
    path('export/eca/pdf/', views.export_eca_pdf, name='export_eca_pdf'),
    path('export/dpp/xlsx/', views.export_dpp_xlsx, name='export_dpp_xlsx'),
    path('export/dpp/pdf/', views.export_dpp_pdf, name='export_dpp_pdf'),
    path('export/reminder/xlsx/', views.export_reminder_xlsx, name='export_reminder_xlsx'),
    path('export/reminder/pdf/', views.export_reminder_pdf, name='export_reminder_pdf'),
    path('export/compensation/xlsx/', views.export_compensation_xlsx, name='export_compensation_xlsx'),
    path('export/compensation/pdf/', views.export_compensation_pdf, name='export_compensation_pdf'),
    path('export/proof/xlsx/', views.export_proof_xlsx, name='export_proof_xlsx'),
    path('export/proof/pdf/', views.export_proof_pdf, name='export_proof_pdf'),
]
