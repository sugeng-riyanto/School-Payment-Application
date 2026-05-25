from django.urls import path
from . import views

app_name = 'compliance'

urlpatterns = [
    path('', views.compliance_dashboard, name='dashboard'),
    path('audit-log/', views.audit_log_list, name='audit_log_list'),
    path('audit-log/export/xlsx/', views.export_audit_log_xlsx, name='export_audit_xlsx'),
    path('audit-log/export/pdf/', views.export_audit_log_pdf, name='export_audit_pdf'),
    path('compliance/export/xlsx/', views.export_compliance_xlsx, name='export_compliance_xlsx'),
    path('seed/', views.seed_compliance_checklist, name='seed'),
]
