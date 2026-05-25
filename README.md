# Aplikasi Pembayaran Sekolah

Sistem pembayaran sekolah multi-level (SD, SMP, SMA) dengan manajemen peran, approval, dan verifikasi dokumen.

## Fitur Utama
- **Multi-level**: SD, SMP, SMA — setiap level punya kepala sekolah, TU, VP Activity, PIC Teacher, ECA Director sendiri
- **Manajemen Pembayaran**: SPP, DPP, Uang Kegiatan, Cambridge Assessment, ECA
- **Approval Workflow**: TU approve → system generate invoice → parent download
- **QR Verification**: Setiap invoice (tagihan & penerimaan) punya QR code yang bisa diverifikasi di `/info/verify/`
- **Blast Email**: Kirim pengumuman ke dashboard parent & email per level
- **Compliance Dashboard**: SOC 2 Type II, UU PDP No. 27/2022, PCI DSS

## Teknologi
- Django 6.0, Python 3.12
- SQLite (development) / PostgreSQL (production)
- Midtrans Payment Gateway
- Chart.js untuk grafik
- xhtml2pdf untuk generate PDF

## Instalasi
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Akun Demo
| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| TU SD | `tu_sd` | `tu_sd123` |
| TU SMP | `tu_smp` | `tu_smp123` |
| TU SMA | `tu_sma` | `tu_sma123` |
| Kepsek SD | `kepsek_sd` | `kepsek_sd123` |
| Kepsek SMP | `kepsek_smp` | `kepsek_smp123` |
| Kepsek SMA | `kepsek_sma` | `kepsek_sma123` |
| Parent SD | `parent_demo_sd` | `siswa123` |
| Parent SMP | `parent_demo_smp` | `siswa123` |
| Parent SMA | `parent_demo_sma` | `siswa123` |

## Lisensi
Hak Cipta © 2026 — Sugeng Riyanto
