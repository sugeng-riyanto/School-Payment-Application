from django.db import models
from accounts.models import Grade, AcademicYear, Student


class ECAType(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'ECA Type'
        verbose_name_plural = 'ECA Types'

    def __str__(self):
        return self.name


class ECAProgram(models.Model):
    DURATION_CHOICES = [
        ('1month', '1 Bulan'),
        ('3months', '3 Bulan'),
        ('6months', '6 Bulan'),
        ('1year', '1 Tahun'),
    ]
    eca_type = models.ForeignKey(ECAType, on_delete=models.CASCADE, related_name='programs')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='eca_programs')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='eca_programs')
    price = models.DecimalField(max_digits=12, decimal_places=0)
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES)
    max_participants = models.IntegerField(default=0)
    is_open = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False, verbose_name='Disetujui Director')
    approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_eca_programs')
    schedule = models.TextField(blank=True, help_text='Jadwal kegiatan rutin')
    schedule2 = models.TextField(blank=True, help_text='Jadwal kegiatan tambahan')
    pic = models.CharField(max_length=200, blank=True, help_text='Penanggung jawab')
    coach_profile = models.TextField(blank=True, help_text='Profil pelatih / instruktur')
    rules = models.TextField(blank=True, help_text='Ketentuan dan tata tertib')
    additional_info = models.TextField(blank=True, help_text='Informasi penting lainnya')
    meeting_link = models.URLField(blank=True, help_text='Link Google Meet / Zoom jika online')
    location = models.CharField(max_length=200, blank=True, help_text='Lokasi kegiatan')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'ECA Program'
        verbose_name_plural = 'ECA Programs'

    def __str__(self):
        return f"{self.name} - {self.grade} ({self.academic_year})"


class ECARegistration(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Disetujui'),
        ('rejected', 'Ditolak'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='eca_registrations')
    program = models.ForeignKey(ECAProgram, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rejection_notes = models.TextField(blank=True, verbose_name='Catatan Penolakan')
    reviewed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_eca_registrations')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'ECA Registration'
        verbose_name_plural = 'ECA Registrations'
        unique_together = ['student', 'program']

    def __str__(self):
        return f"{self.student.full_name} - {self.program.name}"


class ECAScore(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='eca_scores')
    program = models.ForeignKey(ECAProgram, on_delete=models.CASCADE, related_name='scores')
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True, help_text='Keterangan')
    scored_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ECA Score'
        verbose_name_plural = 'ECA Scores'
        unique_together = ['student', 'program']

    def __str__(self):
        return f"{self.student.full_name} - {self.program.name}: {self.score}"


class ECAReport(models.Model):
    PERIOD_CHOICES = [
        ('monthly', 'Bulanan'),
        ('semester', 'Semester'),
        ('final', 'Akhir Tahun'),
    ]
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='eca_reports')
    program = models.ForeignKey(ECAProgram, on_delete=models.CASCADE, related_name='reports')
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    total_students = models.IntegerField(default=0)
    total_paid = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'), ('submitted', 'Diajukan'),
        ('approved', 'Disetujui'), ('revised', 'Revisi'), ('rejected', 'Ditolak'),
    ], default='draft')
    rejection_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_eca_reports')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Laporan ECA'
        verbose_name_plural = 'Laporan ECA'

    def __str__(self):
        return f"ECA Report - {self.program.name} ({self.get_period_display()})"


class ECAPayment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Diterima'),
        ('revised', 'Revisi'),
        ('rejected', 'Ditolak'),
    ]
    registration = models.ForeignKey(ECARegistration, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=0, default=0, help_text='Jumlah yang dibayarkan')
    is_paid = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_notes = models.TextField(blank=True, help_text='Catatan review pembayaran')
    under_over_amount = models.DecimalField(max_digits=12, decimal_places=0, default=0, help_text='Kelebihan (+) / Kekurangan (-)')
    paid_at = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    reviewed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='eca_payment_reviews')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.registration.student.full_name} - {self.registration.program.name}: Rp{self.amount:,}"


class ECAInvoice(models.Model):
    registration = models.ForeignKey(ECARegistration, on_delete=models.CASCADE, related_name='invoices')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='eca_invoices')
    invoice_number = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    pdf = models.FileField(upload_to='eca_invoices/', blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'ECA Invoice'
        verbose_name_plural = 'ECA Invoices'

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.student.full_name}"


class ECASetting(models.Model):
    max_selection = models.IntegerField(default=3, help_text='Maksimal jumlah ECA yang bisa dipilih per siswa')

    class Meta:
        verbose_name = 'Pengaturan ECA'
        verbose_name_plural = 'Pengaturan ECA'

    def __str__(self):
        return f'Max selection: {self.max_selection}'
