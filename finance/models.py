from django.db import models
from accounts.models import Student, AcademicYear


class SPP(models.Model):
    MONTH_CHOICES = [
        (1, 'Januari'), (2, 'Februari'), (3, 'Maret'),
        (4, 'April'), (5, 'Mei'), (6, 'Juni'),
        (7, 'Juli'), (8, 'Agustus'), (9, 'September'),
        (10, 'Oktober'), (11, 'November'), (12, 'Desember'),
    ]
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='spp_rates')
    grade = models.ForeignKey('accounts.Grade', on_delete=models.CASCADE, related_name='spp_rates')
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'SPP Rate'
        verbose_name_plural = 'SPP Rates'
        unique_together = ['academic_year', 'grade']

    def __str__(self):
        return f"SPP {self.grade} - {self.academic_year}: Rp{self.amount:,}"


class SPPBill(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='spp_bills')
    spp = models.ForeignKey(SPP, on_delete=models.CASCADE, related_name='bills')
    month = models.IntegerField(choices=SPP.MONTH_CHOICES)
    year = models.IntegerField()
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    virtual_account = models.CharField(max_length=50, blank=True)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    verification_code = models.CharField(max_length=20, blank=True, verbose_name='Kode Verifikasi')

    class Meta:
        verbose_name = 'SPP Bill'
        verbose_name_plural = 'SPP Bills'
        unique_together = ['student', 'month', 'year']

    def __str__(self):
        return f"SPP {self.student.full_name} - {self.get_month_display()} {self.year}"


class DPP(models.Model):
    CATEGORY_CHOICES = [
        ('pembangunan', 'DPP Pembangunan'),
        ('kegiatan', 'Uang Kegiatan'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='dpp_payments')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Disetujui'),
        ('revised', 'Revisi'),
        ('rejected', 'Ditolak'),
    ], default='pending')
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    payment_proof = models.ImageField(upload_to='dpp_proofs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'DPP Payment'
        verbose_name_plural = 'DPP Payments'

    def __str__(self):
        return f"{self.get_category_display()} - {self.student.full_name}: Rp{self.amount:,}"


class SPPReport(models.Model):
    PERIOD_CHOICES = [
        ('monthly', 'Bulanan'),
    ]
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='spp_reports')
    grade = models.ForeignKey('accounts.Grade', on_delete=models.CASCADE, related_name='spp_reports')
    month = models.IntegerField(choices=SPP.MONTH_CHOICES)
    year = models.IntegerField()
    total_bills = models.IntegerField(default=0)
    total_paid = models.IntegerField(default=0)
    total_amount = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    total_collected = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'), ('submitted', 'Diajukan'),
        ('approved', 'Disetujui'), ('revised', 'Revisi'), ('rejected', 'Ditolak'),
    ], default='draft')
    rejection_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_spp_reports')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Laporan Bulanan SPP'
        verbose_name_plural = 'Laporan Bulanan SPP'

    def __str__(self):
        return f"SPP Report - {self.grade} - {self.get_month_display()} {self.year}"


class DPPReport(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='dpp_reports')
    grade = models.ForeignKey('accounts.Grade', on_delete=models.CASCADE, related_name='dpp_reports')
    category = models.CharField(max_length=20, choices=[
        ('pembangunan', 'DPP Pembangunan'), ('kegiatan', 'Uang Kegiatan'),
    ])
    total_students = models.IntegerField(default=0)
    total_paid = models.IntegerField(default=0)
    total_amount = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    total_collected = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'), ('submitted', 'Diajukan'),
        ('approved', 'Disetujui'), ('revised', 'Revisi'), ('rejected', 'Ditolak'),
    ], default='draft')
    rejection_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_dpp_reports')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Laporan DPP'
        verbose_name_plural = 'Laporan DPP'

    def __str__(self):
        return f"DPP Report - {self.grade} - {self.get_category_display()}"


class Discount(models.Model):
    DISCOUNT_TYPES = [
        ('spp', 'SPP'),
        ('dpp', 'DPP'),
        ('eca', 'ECA'),
        ('kegiatan', 'Uang Kegiatan'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='discounts')
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=0, help_text='Jumlah diskon dalam Rupiah')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    valid_until = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='created_discounts')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Diskon'
        verbose_name_plural = 'Diskon'

    def __str__(self):
        return f'Diskon {self.student.full_name} - {self.get_discount_type_display()}: Rp{self.amount:,}'


class Compensation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='compensations')
    COMP_TYPE_CHOICES = [
        ('spp', 'SPP'),
        ('dpp', 'DPP'),
        ('eca', 'ECA'),
        ('kegiatan', 'Uang Kegiatan'),
        ('other', 'Lainnya'),
    ]
    comp_type = models.CharField(max_length=20, choices=COMP_TYPE_CHOICES)
    DISCOUNT_METHOD_CHOICES = [('nominal', 'Nominal (Rp)'), ('persen', 'Persen (%)')]
    discount_method = models.CharField(max_length=10, choices=DISCOUNT_METHOD_CHOICES, default='nominal')
    description = models.TextField()
    original_amount = models.DecimalField(max_digits=12, decimal_places=0)
    comp_amount = models.DecimalField(max_digits=12, decimal_places=0, help_text='Jumlah kompensasi/potongan (Rp atau %)')
    final_amount = models.DecimalField(max_digits=12, decimal_places=0, editable=False)
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='created_compensations')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Kompensasi Pembayaran'
        verbose_name_plural = 'Kompensasi Pembayaran'

    def save(self, *args, **kwargs):
        if self.discount_method == 'persen':
            self.final_amount = self.original_amount - (self.original_amount * self.comp_amount / 100)
        else:
            self.final_amount = self.original_amount - self.comp_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Kompensasi {self.student.full_name} - {self.get_comp_type_display()}: Rp{self.comp_amount:,}"


class CambridgeAssessment(models.Model):
    EXAM_CHOICES = [
        ('checkpoints', 'Checkpoints'),
        ('igcse', 'IGCSE'),
        ('as_level', 'AS Level'),
        ('a_level', 'A Level'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='cambridge_payments')
    exam_type = models.CharField(max_length=20, choices=EXAM_CHOICES)
    subject = models.CharField(max_length=100, verbose_name='Mata Pelajaran')
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cambridge Assessment'
        verbose_name_plural = 'Cambridge Assessment'

    def __str__(self):
        return f"{self.student.full_name} - {self.get_exam_type_display()} {self.subject}"


class CambridgeFee(models.Model):
    EXAM_CHOICES = [
        ('checkpoints', 'Checkpoints'),
        ('igcse', 'IGCSE'),
        ('as_level', 'AS Level'),
        ('a_level', 'A Level'),
    ]
    exam_type = models.CharField(max_length=20, choices=EXAM_CHOICES)
    subject = models.CharField(max_length=100, verbose_name='Mata Pelajaran', default='All')
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tarif Cambridge'
        verbose_name_plural = 'Tarif Cambridge'
        unique_together = ['exam_type', 'subject']

    def __str__(self):
        return f'{self.get_exam_type_display()} - {self.subject}: Rp{self.amount:,}'


class PaymentReminder(models.Model):
    REMINDER_CHOICES = [
        (1, 'Peringatan Pertama'),
        (2, 'Peringatan Kedua'),
        (3, 'Peringatan Ketiga'),
    ]
    spp_bill = models.ForeignKey(SPPBill, on_delete=models.CASCADE, related_name='reminders', null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payment_reminders')
    reminder_type = models.IntegerField(choices=REMINDER_CHOICES)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='reminders')
    month = models.IntegerField(choices=SPP.MONTH_CHOICES, null=True, blank=True)
    notes = models.TextField(blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Payment Reminder'
        verbose_name_plural = 'Payment Reminders'

    def __str__(self):
        return f"{self.get_reminder_type_display()} - {self.student.full_name}"


class BankAccount(models.Model):
    LEVEL_CHOICES = [
        ('sd', 'SD'),
        ('smp', 'SMP'),
        ('sma', 'SMA'),
    ]
    PAYMENT_TYPE_CHOICES = [
        ('spp', 'SPP'),
        ('dpp_pembangunan', 'DPP Pembangunan'),
        ('uang_kegiatan', 'Uang Kegiatan'),
        ('cambridge', 'Cambridge Assessment'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Menunggu Persetujuan'),
        ('approved', 'Disetujui'),
        ('rejected', 'Ditolak'),
    ]
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, default='spp')
    bank_name = models.CharField(max_length=100, verbose_name='Nama Bank')
    account_number = models.CharField(max_length=50, verbose_name='No. Rekening')
    account_holder = models.CharField(max_length=200, verbose_name='Atas Nama')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_active = models.BooleanField(default=False)
    notes = models.TextField(blank=True, help_text='Catatan persetujuan / penolakan')
    approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_bank_accounts')
    approved_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Rekening Bank'
        verbose_name_plural = 'Rekening Bank'
        unique_together = ['level', 'payment_type']
        ordering = ['level', 'payment_type']

    def __str__(self):
        return f"{self.get_level_display()} - {self.get_payment_type_display()} ({self.bank_name})"
