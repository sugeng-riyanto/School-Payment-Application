from django.db import models
from django.conf import settings
from django.core.files import File


class SchoolProfile(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nama Sekolah')
    address = models.TextField(verbose_name='Alamat Lengkap')
    phone = models.CharField(max_length=50, verbose_name='Nomor Telepon')
    email = models.EmailField(verbose_name='Email Resmi')
    website = models.URLField(blank=True, verbose_name='Website')
    vision = models.TextField(verbose_name='Visi')
    mission = models.TextField(verbose_name='Misi')
    core_values = models.TextField(blank=True, verbose_name='Nilai-nilai Inti')
    history = models.TextField(blank=True, verbose_name='Sejarah Singkat')
    accreditation = models.CharField(max_length=100, blank=True, verbose_name='Akreditasi')
    logo = models.ImageField(upload_to='school/', blank=True, verbose_name='Logo Sekolah')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profil Sekolah'
        verbose_name_plural = 'Profil Sekolah'

    def __str__(self):
        return self.name

    def get_logo_url(self):
        if self.logo and self.logo.storage.exists(self.logo.name):
            return self.logo.url
        return settings.STATIC_URL + 'img/logo_shb.png'

    @classmethod
    def get_profile(cls):
        obj, created = cls.objects.get_or_create(id=1, defaults={'name': 'Sekolah', 'address': '-', 'phone': '-', 'email': '-', 'vision': '-', 'mission': '-'})
        if created or not obj.logo or not obj.logo.storage.exists(obj.logo.name):
            default_path = settings.BASE_DIR / 'static' / 'img' / 'logo_shb.png'
            if default_path.exists():
                with open(str(default_path), 'rb') as f:
                    obj.logo.save('logo_default.png', File(f), save=True)
        return obj


class ContactInfo(models.Model):
    school = models.ForeignKey(SchoolProfile, on_delete=models.CASCADE, related_name='contacts', default=1)
    label = models.CharField(max_length=100, verbose_name='Label (mis: Administrasi, Darurat)')
    contact_type = models.CharField(max_length=20, choices=[('phone', 'Telepon'), ('email', 'Email'), ('whatsapp', 'WhatsApp')])
    value = models.CharField(max_length=200)
    is_emergency = models.BooleanField(default=False, verbose_name='Kontak Darurat')
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Kontak'
        verbose_name_plural = 'Kontak'
        ordering = ['order']

    def __str__(self):
        return f'{self.label}: {self.value}'


class SocialMedia(models.Model):
    school = models.ForeignKey(SchoolProfile, on_delete=models.CASCADE, related_name='social_media', default=1)
    platform = models.CharField(max_length=50, verbose_name='Platform (Instagram, YouTube, dll)')
    url = models.URLField()
    icon = models.CharField(max_length=50, blank=True, help_text='Nama ikon FontAwesome')

    class Meta:
        verbose_name = 'Media Sosial'
        verbose_name_plural = 'Media Sosial'

    def __str__(self):
        return f'{self.platform}'


class CurriculumInfo(models.Model):
    LEVEL_CHOICES = [('sd', 'SD'), ('smp', 'SMP'), ('sma', 'SMA')]
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, verbose_name='Jenjang')
    title = models.CharField(max_length=200, verbose_name='Judul (mis: Kurikulum Merdeka)')
    description = models.TextField(verbose_name='Deskripsi')
    subjects = models.TextField(blank=True, help_text='Daftar mata pelajaran (dipisah koma)')
    pedagogical = models.TextField(blank=True, verbose_name='Pendekatan Pedagogis')
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Informasi Kurikulum'
        verbose_name_plural = 'Informasi Kurikulum'
        ordering = ['level', 'order']

    def __str__(self):
        return f'{self.get_level_display()} - {self.title}'


class SpecialProgram(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nama Program Khusus')
    description = models.TextField(verbose_name='Deskripsi')
    target_level = models.CharField(max_length=50, blank=True, help_text='Target jenjang')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Program Khusus'
        verbose_name_plural = 'Program Khusus'

    def __str__(self):
        return self.name


class TeacherProfile(models.Model):
    LEVEL_CHOICES = [('sd', 'SD'), ('smp', 'SMP'), ('sma', 'SMA')]
    full_name = models.CharField(max_length=200, verbose_name='Nama Lengkap')
    photo = models.ImageField(upload_to='teachers/', blank=True, verbose_name='Foto')
    qualification = models.CharField(max_length=200, verbose_name='Kualifikasi Pendidikan')
    subjects = models.CharField(max_length=300, verbose_name='Mata Pelajaran Diampu')
    position = models.CharField(max_length=200, blank=True, verbose_name='Jabatan')
    email = models.EmailField(blank=True, verbose_name='Email Profesional')
    phone = models.CharField(max_length=50, blank=True, verbose_name='Kontak')
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, blank=True, verbose_name='Jenjang')
    nip = models.CharField(max_length=50, blank=True, verbose_name='NIP')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Profil Guru'
        verbose_name_plural = 'Profil Guru'
        ordering = ['order']

    def __str__(self):
        return self.full_name


class TeacherStructure(models.Model):
    LEVEL_CHOICES = [('sd', 'SD'), ('smp', 'SMP'), ('sma', 'SMA')]
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, unique=True, verbose_name='Jenjang')
    image = models.ImageField(upload_to='structures/', verbose_name='Gambar Struktur Organisasi')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Struktur Guru'
        verbose_name_plural = 'Struktur Guru'

    def __str__(self):
        return f'Struktur {self.get_level_display()}'


class SchoolLevelInfo(models.Model):
    LEVEL_CHOICES = [('sd', 'SD'), ('smp', 'SMP'), ('sma', 'SMA')]
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, unique=True, verbose_name='Jenjang')
    accreditation = models.CharField(max_length=100, blank=True, verbose_name='Akreditasi')
    accreditation_link = models.URLField(blank=True, verbose_name='Link Akreditasi')
    accreditation_valid_from = models.DateField(null=True, blank=True, verbose_name='Akreditasi Berlaku Dari')
    izin_operasional = models.CharField(max_length=200, blank=True, verbose_name='Izin Operasional')
    izin_valid_from = models.DateField(null=True, blank=True, verbose_name='Izin Operasional Berlaku Dari')

    class Meta:
        verbose_name = 'Informasi Jenjang'
        verbose_name_plural = 'Informasi Jenjang'

    def __str__(self):
        return f'{self.get_level_display()}'


class GradingInfo(models.Model):
    LEVEL_CHOICES = [('sd', 'SD'), ('smp', 'SMP'), ('sma', 'SMA')]
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, verbose_name='Jenjang')
    title = models.CharField(max_length=200, verbose_name='Judul')
    description = models.TextField(verbose_name='Penjelasan Sistem Penilaian')
    grading_scale = models.TextField(blank=True, help_text='Skala nilai (A/B/C/dll)')
    report_guide = models.TextField(blank=True, verbose_name='Panduan Interpretasi Rapor')
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Sistem Penilaian'
        verbose_name_plural = 'Sistem Penilaian'
        ordering = ['level', 'order']

    def __str__(self):
        return f'{self.get_level_display()} - {self.title}'
