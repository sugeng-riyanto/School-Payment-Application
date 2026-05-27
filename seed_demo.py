import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()

from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
import random

from accounts.models import User, AcademicYear, Grade, ClassGrade, Student
from finance.models import SPP, SPPBill, DPP, CambridgeFee, CambridgeAssessment, BankAccount, Discount, Compensation
from eca.models import ECAType, ECAProgram, ECARegistration, ECASetting
from payments.models import MidtransConfig, PaymentTransaction, BlastEmailTemplate

today = date.today()

PASS = 'admin123'

# ============================================================
# 1. ACADEMIC YEAR
# ============================================================
ay, _ = AcademicYear.objects.get_or_create(
    name='2025/2026',
    defaults={'is_active': True, 'start_date': date(2025, 7, 1), 'end_date': date(2026, 6, 30)}
)
if not ay.is_active:
    ay.is_active = True
    ay.save()

# ============================================================
# 2. GRADES
# ============================================================
grades = {}
for level, name in [('sd', 'SD'), ('smp', 'SMP'), ('sma', 'SMA')]:
    g, _ = Grade.objects.get_or_create(level=level, defaults={'name': name})
    grades[level] = g
print(f'Grades: {[(g.name, g.level) for g in grades.values()]}')

# ============================================================
# 3. CLASSGRADES
# ============================================================
class_data = {
    'sd': ['Kelas 1 SD', 'Kelas 2 SD', 'Kelas 3 SD', 'Kelas 4 SD', 'Kelas 5 SD', 'Kelas 6 SD'],
    'smp': ['Kelas 7 SMP', 'Kelas 8 SMP', 'Kelas 9 SMP'],
    'sma': ['Kelas 10 SMA', 'Kelas 11 SMA', 'Kelas 12 SMA'],
}
created_classes = []
for level, class_names in class_data.items():
    for name in class_names:
        cg, _ = ClassGrade.objects.get_or_create(name=name, grade=grades[level], academic_year=ay)
        created_classes.append(cg)
print(f'ClassGrades: {len(created_classes)}')

# ============================================================
# 4. USERS (create if not exist on SQLite)
# ============================================================
def _make_user(email, role, level, first, last):
    u, created = User.objects.get_or_create(
        email=email,
        defaults={
            'username': email.split('@')[0],
            'role': role, 'assigned_level': level,
            'first_name': first, 'last_name': last,
            'phone': '081234567890', 'show_phone': True,
            'alamat': 'Alamat Demo',
        }
    )
    if created:
        u.set_password(PASS)
        u.save()
    return u, created

admin_user, _    = _make_user('sugeng.riyanto@shb.sch.id', 'admin', '', 'Sugeng', 'Riyanto')
_make_user('admin@school.com', 'admin', '', 'Admin', 'Cadangan')
parent, _       = _make_user('srphysics04@gmail.com', 'parent', '', 'Orang Tua', 'Demo')
vp_user, _      = _make_user('aqeelainstruments@gmail.com', 'vp_activity', 'sd', 'VP', 'Activity')
kepsek_user, _  = _make_user('shsmodernhill@shb.sch.id', 'kepsek', 'sd', 'Kepsek', 'SHB')
tu_user, _      = _make_user('tu@shb.sch.id', 'tu', 'sd_smp_sma', 'TU', 'SHB')
eca_user, _     = _make_user('eca@shb.sch.id', 'eca_director', 'sd', 'ECA', 'Director')
pic_user, _     = _make_user('pic@shb.sch.id', 'pic_teacher', 'sd', 'PIC', 'Teacher')

print(f'Users ready (password {PASS})')

# ============================================================
# 4. STUDENTS (3 children for parent)
# ============================================================
students_data = [
    {'nisn': '0000000001', 'nis': 'NISSD001', 'full_name': 'Siswa SD Demo', 'class_grade_name': 'Kelas 6 SD'},
    {'nisn': '0000000002', 'nis': 'NISSMP001', 'full_name': 'Siswa SMP Demo', 'class_grade_name': 'Kelas 9 SMP'},
    {'nisn': '0000000003', 'nis': 'NISSMA001', 'full_name': 'Siswa SMA Demo', 'class_grade_name': 'Kelas 12 SMA'},
]
students = []
for sd in students_data:
    cg = ClassGrade.objects.get(name=sd['class_grade_name'], academic_year=ay)
    s, _ = Student.objects.get_or_create(
        nisn=sd['nisn'],
        defaults={
            'nis': sd['nis'],
            'full_name': sd['full_name'],
            'parent': parent,
            'class_grade': cg,
            'place_of_birth': 'Jakarta',
            'date_of_birth': date(2010, 1, 1),
            'address': 'Jl. Contoh No. 1, Jakarta',
            'is_active': True,
        }
    )
    students.append(s)
    print(f'Student: {s.full_name} ({s.nisn}) -> {cg.name}')

# ============================================================
# 5. SPP TARIF (per grade level)
# ============================================================
spp_rates = [
    (grades['sd'], Decimal('250000')),
    (grades['smp'], Decimal('350000')),
    (grades['sma'], Decimal('500000')),
]
spp_objects = []
for grade, amount in spp_rates:
    s, _ = SPP.objects.get_or_create(academic_year=ay, grade=grade, defaults={'amount': amount, 'is_active': True})
    spp_objects.append(s)
    print(f'SPP tarif: {grade.name} = Rp{amount}')

# ============================================================
# 6. SPP BILLS (generate for 3 months: Juli, Agustus, September)
# ============================================================
months = [7, 8, 9]  # Juli, Agustus, September
bills_created = 0
for student in students:
    grade = student.class_grade.grade
    spp = SPP.objects.get(academic_year=ay, grade=grade)
    for month in months:
        bill, created = SPPBill.objects.get_or_create(
            student=student, month=month, year=2025,
            defaults={
                'spp': spp,
                'amount': spp.amount,
                'due_date': date(2025, month, 15),
                'virtual_account': f'VA{student.nisn}{month:02d}2025',
                'verification_code': f'SPP{student.nisn}{month:02d}',
            }
        )
        if created:
            bills_created += 1
print(f'SPP Bills: {bills_created} created')

# ============================================================
# 7. DPP PEMBANGUNAN (one-time per student)
# ============================================================
dpp_data = [
    (students[0], Decimal('1500000'), 'DPP Pembangunan SD - Tahun Ajaran 2025/2026'),
    (students[1], Decimal('2000000'), 'DPP Pembangunan SMP - Tahun Ajaran 2025/2026'),
    (students[2], Decimal('3000000'), 'DPP Pembangunan SMA - Tahun Ajaran 2025/2026'),
]
for student, amount, desc in dpp_data:
    DPP.objects.get_or_create(
        student=student, category='pembangunan', amount=amount,
        defaults={'description': desc, 'status': 'approved', 'is_paid': False}
    )
print(f'DPP Pembangunan: {len(dpp_data)} created')

# ============================================================
# 8. UANG KEGIATAN (one-time per student)
# ============================================================
kegiatan_data = [
    (students[0], Decimal('300000'), 'Uang Kegiatan SD - Studi Tour'),
    (students[1], Decimal('500000'), 'Uang Kegiatan SMP - Outbound'),
    (students[2], Decimal('750000'), 'Uang Kegiatan SMA - Perpisahan'),
]
for student, amount, desc in kegiatan_data:
    DPP.objects.get_or_create(
        student=student, category='kegiatan', amount=amount,
        defaults={'description': desc, 'status': 'approved', 'is_paid': False}
    )
print(f'Uang Kegiatan: {len(kegiatan_data)} created')

# ============================================================
# 9. CAMBRIDGE ASSESSMENT
# ============================================================
# Fee rates
cambridge_fees = [
    ('checkpoints', 'English', Decimal('500000')),
    ('checkpoints', 'Mathematics', Decimal('500000')),
    ('checkpoints', 'Science', Decimal('500000')),
    ('igcse', 'English', Decimal('750000')),
    ('igcse', 'Mathematics', Decimal('750000')),
    ('igcse', 'Physics', Decimal('750000')),
    ('igcse', 'Chemistry', Decimal('750000')),
    ('as_level', 'Mathematics', Decimal('1000000')),
    ('as_level', 'Physics', Decimal('1000000')),
    ('as_level', 'Chemistry', Decimal('1000000')),
]
for exam_type, subject, amount in cambridge_fees:
    CambridgeFee.objects.get_or_create(exam_type=exam_type, subject=subject, defaults={'amount': amount, 'is_active': True})
print(f'Cambridge Fees: {len(cambridge_fees)} created')

# Assessments per student
cambridge_assess = [
    (students[0], 'checkpoints', 'English'),
    (students[0], 'checkpoints', 'Mathematics'),
    (students[0], 'checkpoints', 'Science'),
    (students[1], 'checkpoints', 'English'),
    (students[1], 'checkpoints', 'Mathematics'),
    (students[2], 'igcse', 'English'),
    (students[2], 'igcse', 'Mathematics'),
    (students[2], 'igcse', 'Physics'),
]
for student, exam_type, subject in cambridge_assess:
    fee = CambridgeFee.objects.get(exam_type=exam_type, subject=subject)
    CambridgeAssessment.objects.get_or_create(
        student=student, exam_type=exam_type, subject=subject,
        defaults={'amount': fee.amount, 'is_paid': False}
    )
print(f'Cambridge Assessments: {len(cambridge_assess)} created')

# ============================================================
# 10. ECA TYPES & PROGRAMS (with Midtrans pricing)
# ============================================================
eca_data = [
    {'type': 'Olahraga', 'program': 'Basket', 'level': 'smp', 'price': 200000},
    {'type': 'Olahraga', 'program': 'Futsal', 'level': 'sd', 'price': 150000},
    {'type': 'Olahraga', 'program': 'Bulu Tangkis', 'level': 'sma', 'price': 250000},
    {'type': 'Seni', 'program': 'Tari Tradisional', 'level': 'sd', 'price': 100000},
    {'type': 'Seni', 'program': 'Band', 'level': 'smp', 'price': 200000},
    {'type': 'Seni', 'program': 'Paduan Suara', 'level': 'sma', 'price': 150000},
    {'type': 'Akademik', 'program': 'Klub Matematika', 'level': 'smp', 'price': 100000},
    {'type': 'Akademik', 'program': 'Klub Sains', 'level': 'sma', 'price': 150000},
    {'type': 'Akademik', 'program': 'Robotics', 'level': 'smp', 'price': 300000},
    {'type': 'Akademik', 'program': 'English Club', 'level': 'sma', 'price': 200000},
]

# Ensure max_selection setting
ECASetting.objects.get_or_create(id=1, defaults={'max_selection': 3})

for ed in eca_data:
    t, _ = ECAType.objects.get_or_create(name=ed['type'], defaults={'description': f'Kegiatan {ed["type"]}', 'is_active': True})
    ECAProgram.objects.get_or_create(
        name=ed['program'], eca_type=t, grade=grades[ed['level']], academic_year=ay,
        defaults={
            'description': f'Program {ed["program"]} untuk tingkat {ed["level"].upper()}',
            'price': ed['price'],
            'duration': '1year',
            'max_participants': 30,
            'is_open': True,
            'is_approved': True,
            'approved_by': eca_user,
            'schedule': f'Seminggu 2x, setelah pulang sekolah',
            'pic': 'Coach Professional',
            'location': f'Lapangan/Ruang {ed["program"]}',
        }
    )
print(f'ECA Types & Programs: {len(eca_data)} created')

# Register student for 1 ECA program (midtrans payment)
ecap = ECAProgram.objects.filter(is_open=True, is_approved=True).first()
if ecap:
    ECARegistration.objects.get_or_create(
        student=students[0], program=ecap,
        defaults={'status': 'approved', 'is_paid': False, 'reviewed_by': eca_user}
    )
    print(f'ECA Registration: {students[0].full_name} -> {ecap.name}')

# ============================================================
# 11. BANK ACCOUNTS (approved by Kepsek)
# ============================================================
bank_accounts = [
    {'level': 'sd', 'payment_type': 'spp', 'bank_name': 'Bank Mandiri', 'account_number': '1234567890', 'account_holder': 'Sekolah Harapan Bangsa'},
    {'level': 'sd', 'payment_type': 'dpp_pembangunan', 'bank_name': 'Bank Mandiri', 'account_number': '1234567891', 'account_holder': 'Sekolah Harapan Bangsa'},
    {'level': 'sd', 'payment_type': 'uang_kegiatan', 'bank_name': 'Bank BCA', 'account_number': '9876543210', 'account_holder': 'Sekolah Harapan Bangsa'},
    {'level': 'sd', 'payment_type': 'cambridge', 'bank_name': 'Bank BCA', 'account_number': '9876543211', 'account_holder': 'Sekolah Harapan Bangsa'},
    {'level': 'smp', 'payment_type': 'spp', 'bank_name': 'Bank Mandiri', 'account_number': '1234567892', 'account_holder': 'Sekolah Harapan Bangsa'},
    {'level': 'smp', 'payment_type': 'dpp_pembangunan', 'bank_name': 'Bank Mandiri', 'account_number': '1234567893', 'account_holder': 'Sekolah Harapan Bangsa'},
    {'level': 'smp', 'payment_type': 'uang_kegiatan', 'bank_name': 'Bank BCA', 'account_number': '9876543212', 'account_holder': 'Sekolah Harapan Bangsa'},
    {'level': 'smp', 'payment_type': 'cambridge', 'bank_name': 'Bank BCA', 'account_number': '9876543213', 'account_holder': 'Sekolah Harapan Bangsa'},
    {'level': 'sma', 'payment_type': 'spp', 'bank_name': 'Bank Mandiri', 'account_number': '1234567894', 'account_holder': 'Sekolah Harapan Bangsa'},
    {'level': 'sma', 'payment_type': 'dpp_pembangunan', 'bank_name': 'Bank Mandiri', 'account_number': '1234567895', 'account_holder': 'Sekolah Harapan Bangsa'},
    {'level': 'sma', 'payment_type': 'uang_kegiatan', 'bank_name': 'Bank BCA', 'account_number': '9876543214', 'account_holder': 'Sekolah Harapan Bangsa'},
    {'level': 'sma', 'payment_type': 'cambridge', 'bank_name': 'Bank BCA', 'account_number': '9876543215', 'account_holder': 'Sekolah Harapan Bangsa'},
]
for ba in bank_accounts:
    BankAccount.objects.get_or_create(
        level=ba['level'], payment_type=ba['payment_type'],
        defaults={
            'bank_name': ba['bank_name'],
            'account_number': ba['account_number'],
            'account_holder': ba['account_holder'],
            'status': 'approved',
            'is_active': True,
            'approved_by': kepsek_user,
            'approved_at': timezone.now(),
        }
    )
print(f'Bank Accounts: {len(bank_accounts)} created (approved)')

# ============================================================
# 12. MIDTRANS CONFIG (empty - user will fill via dashboard)
# ============================================================
MidtransConfig.objects.get_or_create(id=1, defaults={
    'merchant_id': '',
    'client_key': '',
    'server_key': '',
    'is_production': False,
})
print('Midtrans Config: created (empty keys)')

# ============================================================
# 13. BLAST EMAIL TEMPLATES
# ============================================================
templates = [
    {'name': 'Template SPP Default', 'payment_type': 'spp', 'subject': 'Informasi Tagihan SPP - {{ student_name }}', 'body': 'Yth. Orang Tua/Wali {{ parent_name }},\n\nBersama ini kami sampaikan tagihan SPP untuk {{ student_name }} sebesar Rp{{ amount }}.\n\nTerima kasih.', 'is_default': True},
    {'name': 'Template Cambridge Default', 'payment_type': 'cambridge', 'subject': 'Informasi Cambridge Assessment - {{ student_name }}', 'body': 'Yth. Orang Tua/Wali {{ parent_name }},\n\nBersama ini kami sampaikan tagihan Cambridge Assessment untuk {{ student_name }}.\n\nTerima kasih.', 'is_default': True},
]
for t in templates:
    BlastEmailTemplate.objects.get_or_create(name=t['name'], defaults={
        'payment_type': t['payment_type'],
        'subject': t['subject'],
        'body': t['body'],
        'is_default': t['is_default'],
        'created_by': admin_user,
    })
print(f'Blast Templates: {len(templates)} created')

# ============================================================
# SUMMARY
# ============================================================
print()
print('=' * 50)
print('SEED DATA COMPLETE')
print('=' * 50)
print(f'  Students: {Student.objects.count()}')
print(f'  SPP Tarifs: {SPP.objects.count()}')
print(f'  SPP Bills: {SPPBill.objects.count()}')
print(f'  DPP (Pembangunan): {DPP.objects.filter(category="pembangunan").count()}')
print(f'  DPP (Kegiatan): {DPP.objects.filter(category="kegiatan").count()}')
print(f'  Cambridge Fees: {CambridgeFee.objects.count()}')
print(f'  Cambridge Assessments: {CambridgeAssessment.objects.count()}')
print(f'  Bank Accounts: {BankAccount.objects.count()}')
print(f'  ECA Types: {ECAType.objects.count()}')
print(f'  ECA Programs: {ECAProgram.objects.count()}')
print(f'  Midtrans Config: {MidtransConfig.objects.count()}')
