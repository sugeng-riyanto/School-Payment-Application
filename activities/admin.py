from django.contrib import admin
from .models import ActivityType, ActivityReport, ActivityIncomeExpense, ActivityEvidence


@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'month', 'budget', 'time_start', 'time_finish', 'created_by')
    list_filter = ('month',)
    search_fields = ('name',)


class ActivityIncomeExpenseInline(admin.TabularInline):
    model = ActivityIncomeExpense
    extra = 1


class ActivityEvidenceInline(admin.TabularInline):
    model = ActivityEvidence
    extra = 1


@admin.register(ActivityReport)
class ActivityReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'pic', 'status', 'created_at')
    list_filter = ('status', 'academic_year')
    search_fields = ('title', 'pic__username')
    inlines = [ActivityIncomeExpenseInline, ActivityEvidenceInline]
    fieldsets = (
        ('Informasi Kegiatan', {'fields': ('activity_type', 'title', 'description', 'start_date', 'end_date', 'pic', 'academic_year', 'cover_image')}),
        ('Dokumentasi', {'fields': ('google_drive_link1', 'google_drive_link2', 'invoice_number')}),
        ('Refleksi & Evaluasi', {'fields': ('reflection', 'evaluation', 'budget_real', 'pic_notes')}),
        ('Tanda Tangan', {'fields': ('signature_data', 'pic_signature_data', 'pic_reviewed_by', 'pic_reviewed_at')}),
        ('Status', {'fields': ('status', 'rejection_notes', 'reviewed_by', 'reviewed_at')}),
    )
