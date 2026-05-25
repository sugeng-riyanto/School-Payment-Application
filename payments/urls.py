from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('create/<str:type>/<int:type_id>/', views.create_payment, name='create'),
    path('midtrans-callback/', views.midtrans_callback, name='midtrans_callback'),
    path('upload-proof/<int:bill_id>/', views.upload_proof, name='upload_proof'),
    path('upload-proof/transaction/<int:tx_id>/', views.upload_proof_for_transaction, name='upload_proof_tx'),
    path('history/', views.payment_history, name='history'),
    path('proofs/', views.proof_list, name='proof_list'),
    path('proofs/<int:proof_id>/verify/', views.verify_proof, name='verify_proof'),
    path('midtrans-config/', views.midtrans_config, name='midtrans_config'),
    path('midtrans-config/test/', views.test_midtrans_connection, name='test_midtrans'),
    path('eca-payment/', views.eca_bulk_payment, name='eca_bulk_payment'),
    path('eca-payment/<int:reg_id>/', views.eca_payment, name='eca_payment'),
    path('eca-payment/<slug:slug>-<int:reg_id>/', views.eca_payment, name='eca_payment_slug'),
    path('cambridge/<int:ca_id>/pay/', views.cambridge_payment, name='cambridge_payment'),
    path('invoice/<int:pk>/download/', views.download_invoice, name='download_invoice'),
    path('va/<int:tx_id>/download/', views.download_va, name='download_va'),
    path('bill/<int:bill_id>/invoice/', views.download_bill_invoice, name='download_bill_invoice'),
    path('export/xlsx/', views.export_history_xlsx, name='export_history_xlsx'),
    path('export/pdf/', views.export_history_pdf, name='export_history_pdf'),
    path('verify-invoice/', views.verify_invoice, name='verify_invoice'),
]
