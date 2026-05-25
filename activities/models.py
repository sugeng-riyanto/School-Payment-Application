from django.db import models
from accounts.models import User, AcademicYear


class ActivityType(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nama Kegiatan')
    objectives = models.TextField(verbose_name='Objectives/Goal')
    values_knowledge = models.TextField(blank=True, verbose_name='Value Knowledge')
    values_faith = models.TextField(blank=True, verbose_name='Value Faith')
    values_character = models.TextField(blank=True, verbose_name='Value Character')
    budget = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='Budget')
    month = models.CharField(max_length=20, verbose_name='Bulan', help_text='Bulan pelaksanaan')
    time_start = models.DateField(verbose_name='Time Start')
    time_finish = models.DateField(verbose_name='Time Finish')
    pic = models.CharField(max_length=200, blank=True, verbose_name='PIC')
    notes = models.TextField(blank=True, verbose_name='Notes')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_types_created')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Jenis Kegiatan'
        verbose_name_plural = 'Jenis Kegiatan'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ActivityReport(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Diajukan ke PIC'),
        ('pic_approved', 'Disetujui PIC'),
        ('approved', 'Disetujui'),
        ('revised', 'Revisi'),
        ('rejected', 'Ditolak'),
    ]
    activity_type = models.ForeignKey(ActivityType, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports', verbose_name='Jenis Kegiatan')
    title = models.CharField(max_length=200)
    description = models.TextField(verbose_name='Deskripsi kegiatan')
    start_date = models.DateField(verbose_name='Tanggal mulai')
    end_date = models.DateField(null=True, blank=True, verbose_name='Tanggal selesai')
    pic = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_reports', limit_choices_to={'role': 'pic_teacher'})
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='activity_reports')
    cover_image = models.ImageField(upload_to='kegiatan/', blank=True)

    google_drive_link1 = models.URLField(blank=True, verbose_name='Link Google Drive 1')
    google_drive_link2 = models.URLField(blank=True, verbose_name='Link Google Drive 2')
    invoice_number = models.CharField(max_length=100, blank=True, verbose_name='Nomor bukti/invoice')
    signature_data = models.TextField(blank=True, help_text='Data tanda tangan canvas (base64) - dari PIC')
    reflection = models.TextField(blank=True, verbose_name='Refleksi')
    evaluation = models.TextField(blank=True, verbose_name='Evaluasi')

    budget_real = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='Budget Realisasi')
    pic_notes = models.TextField(blank=True, verbose_name='Catatan PIC')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    slug = models.SlugField(max_length=255, blank=True, unique=False, help_text='URL slug auto-generated from title')
    rejection_notes = models.TextField(blank=True, help_text='Catatan revisi/penolakan')
    feedback_notes = models.TextField(blank=True, help_text='Catatan/feedback dari Kepsek / VP Activity')
    feedback_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='activity_feedback_given')
    feedback_at = models.DateTimeField(null=True, blank=True)

    pic_reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pic_reviewed_activities')
    pic_reviewed_at = models.DateTimeField(null=True, blank=True)
    pic_signature_data = models.TextField(blank=True, help_text='Tanda tangan PIC (base64)')

    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_activities')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Laporan Kegiatan'
        verbose_name_plural = 'Laporan Kegiatan'
        ordering = ['-start_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base = slugify(self.title)[:200]
            if self.pk:
                self.slug = f"{base}-{self.pk}"
            else:
                self.slug = f"{base}-{id(self)}"
        super().save(*args, **kwargs)
        if self.pk and not self.slug.endswith(f'-{self.pk}'):
            from django.utils.text import slugify
            self.slug = f"{slugify(self.title)[:200]}-{self.pk}"
            super().save(update_fields=['slug'])


class ActivityIncomeExpense(models.Model):
    TRANSACTION_TYPE = [
        ('income', 'Pemasukan'),
        ('expense', 'Pengeluaran'),
    ]
    activity = models.ForeignKey(ActivityReport, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    date = models.DateField()

    class Meta:
        verbose_name = 'Transaksi Kegiatan'
        verbose_name_plural = 'Transaksi Kegiatan'

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.description}: Rp{self.amount:,}"


class ActivityEvidence(models.Model):
    activity = models.ForeignKey(ActivityReport, on_delete=models.CASCADE, related_name='evidences')
    file = models.FileField(upload_to='laporan/', verbose_name='File bukti')
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Bukti Laporan'
        verbose_name_plural = 'Bukti Laporan'

    def __str__(self):
        return f"Evidence - {self.activity.title}"
