from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view_sensitive', 'View Sensitive Data'),
        ('export', 'Export Data'),
        ('payment_verify', 'Payment Verification'),
        ('payment_process', 'Payment Process'),
        ('user_mgmt', 'User Management'),
        ('report_review', 'Report Review'),
        ('data_import', 'Data Import'),
        ('data_export', 'Data Export'),
        ('login_failed', 'Login Failed'),
        ('permission_denied', 'Permission Denied'),
        ('password_change', 'Password Change'),
        ('consent', 'Consent Action'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    username = models.CharField(max_length=150, blank=True)
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100, blank=True)
    object_id = models.CharField(max_length=50, blank=True)
    object_repr = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    request_method = models.CharField(max_length=10, blank=True)
    request_path = models.CharField(max_length=500, blank=True)
    is_sensitive = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.created_at.strftime('%Y-%m-%d %H:%M')} | {self.username} | {self.action} | {self.model_name}"


class SecurityEvent(models.Model):
    EVENT_TYPES = [
        ('access_anomaly', 'Access Anomaly'),
        ('failed_login', 'Failed Login Attempt'),
        ('unauthorized_access', 'Unauthorized Access Attempt'),
        ('data_breach', 'Data Breach Indicator'),
        ('policy_violation', 'Policy Violation'),
        ('encryption_issue', 'Encryption Issue'),
        ('session_anomaly', 'Session Anomaly'),
    ]
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='low')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_events')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Security Event'
        verbose_name_plural = 'Security Events'
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_severity_display()}] {self.title}"


class DataRetentionPolicy(models.Model):
    CATEGORY_CHOICES = [
        ('audit_log', 'Audit Logs'),
        ('payment_transaction', 'Payment Transactions'),
        ('blast_email', 'Blast Email Logs'),
        ('student_data', 'Student Data'),
        ('user_account', 'User Accounts'),
        ('activity_report', 'Activity Reports'),
        ('payment_proof', 'Payment Proofs'),
    ]
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, unique=True)
    retention_days = models.IntegerField(default=365)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Data Retention Policy'
        verbose_name_plural = 'Data Retention Policies'

    def __str__(self):
        return f"{self.get_category_display()}: {self.retention_days} days"


class PrivacyConsent(models.Model):
    CONSENT_TYPES = [
        ('data_processing', 'Data Processing'),
        ('marketing', 'Marketing Communication'),
        ('third_party', 'Third Party Sharing'),
        ('terms_of_service', 'Terms of Service'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='consents')
    consent_type = models.CharField(max_length=30, choices=CONSENT_TYPES)
    is_granted = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    granted_at = models.DateTimeField(auto_now_add=True)
    revoked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Privacy Consent'
        verbose_name_plural = 'Privacy Consents'
        unique_together = ['user', 'consent_type']

    def __str__(self):
        status = 'Granted' if self.is_granted else 'Revoked'
        return f"{self.user.username} - {self.get_consent_type_display()} ({status})"


class ComplianceChecklist(models.Model):
    FRAMEWORK_CHOICES = [
        ('soc2', 'SOC 2 Type II'),
        ('pdp', 'UU PDP No. 27/2022'),
        ('pci_dss', 'PCI DSS'),
    ]
    framework = models.CharField(max_length=10, choices=FRAMEWORK_CHOICES)
    control_id = models.CharField(max_length=50)
    control_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('partial', 'Partially Compliant'),
        ('not_applicable', 'N/A'),
        ('not_assessed', 'Not Assessed'),
    ], default='not_assessed')
    notes = models.TextField(blank=True)
    last_assessed = models.DateTimeField(null=True, blank=True)
    assessed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Compliance Checklist'
        verbose_name_plural = 'Compliance Checklists'
        unique_together = ['framework', 'control_id']
        ordering = ['framework', 'control_id']

    def __str__(self):
        return f"[{self.get_framework_display()}] {self.control_id}: {self.control_name}"
