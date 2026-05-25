from django.db import models
from accounts.models import Student, User


class MidtransConfig(models.Model):
    merchant_id = models.CharField(max_length=50, default='')
    client_key = models.CharField(max_length=200, default='')
    server_key = models.CharField(max_length=200, default='')
    is_production = models.BooleanField(default=False)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='midtrans_updates')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Midtrans Configuration'
        verbose_name_plural = 'Midtrans Configuration'

    def __str__(self):
        return f'Midtrans Config ({"Production" if self.is_production else "Sandbox"})'

    @classmethod
    def get_config(cls):
        config, _ = cls.objects.get_or_create(id=1)
        return config


class PaymentTransaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('expired', 'Expired'),
        ('refund', 'Refund'),
    ]
    TRANSACTION_TYPES = [
        ('spp', 'SPP'),
        ('dpp', 'DPP Pembangunan'),
        ('eca', 'ECA'),
        ('kegiatan', 'Uang Kegiatan'),
        ('cambridge', 'Cambridge Assessment'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payment_transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    midtrans_order_id = models.CharField(max_length=100, unique=True, blank=True)
    midtrans_transaction_id = models.CharField(max_length=100, blank=True)
    midtrans_redirect_url = models.URLField(blank=True)
    snap_token = models.CharField(max_length=500, blank=True)
    virtual_account = models.CharField(max_length=100, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    invoice_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    verification_code = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name='Kode Verifikasi')
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Payment Transaction'
        verbose_name_plural = 'Payment Transactions'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.verification_code:
            import uuid
            self.verification_code = uuid.uuid4().hex[:12].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.student.full_name}: Rp{self.amount:,} ({self.status})"


class PaymentProof(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payment_proofs')
    transaction = models.ForeignKey(PaymentTransaction, on_delete=models.SET_NULL, null=True, blank=True, related_name='proofs')
    spp_bill = models.ForeignKey('finance.SPPBill', on_delete=models.SET_NULL, null=True, blank=True, related_name='proofs')
    image = models.FileField(upload_to='bukti_pembayaran/', blank=True, null=True, help_text='Format: JPG, PNG, PDF')
    description = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Payment Proof'
        verbose_name_plural = 'Payment Proofs'

    def __str__(self):
        return f"Bukti - {self.student.full_name} ({self.uploaded_at.date()})"


class BlastEmailLog(models.Model):
    TYPE_CHOICES = [
        ('spp', 'SPP'),
        ('kegiatan', 'Uang Kegiatan'),
        ('eca', 'ECA'),
        ('cambridge', 'Cambridge Assessment'),
        ('seragam', 'Pembayaran Seragam'),
        ('denda', 'Pembayaran Denda'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='blast_emails')
    payment_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    subject = models.CharField(max_length=300)
    body = models.TextField()
    recipient_email = models.EmailField(blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Blast Email Log'
        verbose_name_plural = 'Blast Email Logs'
        ordering = ['-sent_at']

    def __str__(self):
        return f"[{self.get_payment_type_display()}] {self.student.full_name} - {self.sent_at.date()}"


class BlastEmailTemplate(models.Model):
    TYPE_CHOICES = [
        ('spp', 'SPP'),
        ('kegiatan', 'Uang Kegiatan'),
        ('eca', 'ECA'),
        ('cambridge', 'Cambridge Assessment'),
        ('seragam', 'Pembayaran Seragam'),
        ('denda', 'Pembayaran Denda'),
    ]
    name = models.CharField(max_length=200, verbose_name='Nama Template')
    payment_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='Jenis Pembayaran')
    subject = models.CharField(max_length=300, verbose_name='Subjek Email')
    body = models.TextField(verbose_name='Body Email')
    bank_account = models.CharField(max_length=200, blank=True, verbose_name='Rekening Tujuan')
    is_default = models.BooleanField(default=False, verbose_name='Template Default')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_templates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Template Blast Email'
        verbose_name_plural = 'Template Blast Email'
        ordering = ['-updated_at']

    def __str__(self):
        return self.name
