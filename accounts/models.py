from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('tu', 'Tata Usaha'),
        ('kepsek', 'Kepala Sekolah'),
        ('vp_activity', 'VP Activity'),
        ('pic_teacher', 'PIC Teacher'),
        ('eca_director', 'ECA Director'),
        ('parent', 'Parent'),
    ]
    LEVEL_CHOICES = [
        ('sd', 'SD'),
        ('smp', 'SMP'),
        ('sma', 'SMA'),
        ('sd_smp', 'SD & SMP'),
        ('smp_sma', 'SMP & SMA'),
        ('sd_smp_sma', 'SD, SMP & SMA'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='parent')
    assigned_level = models.CharField(max_length=10, choices=LEVEL_CHOICES, blank=True, help_text='Jenjang akses untuk Kepsek / VP Activity / TU')
    nip = models.CharField(max_length=30, unique=True, blank=True, null=True, verbose_name='NIP', help_text='Nomor Induk Pegawai untuk staf')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Nomor HP')
    alamat = models.TextField(blank=True, verbose_name='Alamat')
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='Foto Profil')
    show_phone = models.BooleanField(default=False, verbose_name='Tampilkan nomor HP di profil')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"


class AcademicYear(models.Model):
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()

    def save(self, *args, **kwargs):
        if self.is_active:
            AcademicYear.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Grade(models.Model):
    LEVEL_CHOICES = [
        ('sd', 'SD'),
        ('smp', 'SMP'),
        ('sma', 'SMA'),
    ]
    name = models.CharField(max_length=50)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)

    def __str__(self):
        return f"{self.get_level_display()} - {self.name}"


class ClassGrade(models.Model):
    name = models.CharField(max_length=50)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='classes')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='classes')

    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    def __str__(self):
        return f"{self.grade} - {self.name} ({self.academic_year})"


class Student(models.Model):
    nisn = models.CharField(max_length=20, primary_key=True, verbose_name='NISN')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children', limit_choices_to={'role': 'parent'})
    class_grade = models.ForeignKey(ClassGrade, on_delete=models.CASCADE, related_name='students')
    nis = models.CharField(max_length=20, unique=True, verbose_name='NIS')
    full_name = models.CharField(max_length=200)
    place_of_birth = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    graduated_at = models.DateTimeField(null=True, blank=True, verbose_name='Tanggal Lulus')

    def __str__(self):
        return f"{self.full_name} ({self.nisn})"


class InternalInfo(models.Model):
    LEVEL_CHOICES = [
        ('sd', 'SD'),
        ('smp', 'SMP'),
        ('sma', 'SMA'),
        ('all', 'Semua Jenjang'),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    level = models.CharField(max_length=50, default='all')
    file = models.FileField(upload_to='internal_info/', blank=True, null=True)
    google_drive_link = models.URLField(blank=True, verbose_name='Tautan Google Drive')
    is_published = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_info')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_info')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Informasi Internal'
        verbose_name_plural = 'Informasi Internal'
        ordering = ['-created_at']

    def get_levels_list(self):
        return self.level.split(',') if self.level else ['all']

    def __str__(self):
        return self.title
