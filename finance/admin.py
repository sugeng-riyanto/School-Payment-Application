from django.contrib import admin
from .models import SPP, SPPBill, DPP, PaymentReminder, SPPReport, DPPReport, Compensation


@admin.register(SPP)
class SPPAdmin(admin.ModelAdmin):
    list_display = ('grade', 'academic_year', 'amount', 'is_active')
    list_filter = ('academic_year', 'grade')


@admin.register(SPPBill)
class SPPBillAdmin(admin.ModelAdmin):
    list_display = ('student', 'month', 'year', 'amount', 'is_paid', 'due_date')
    list_filter = ('is_paid', 'year', 'month')
    search_fields = ('student__full_name',)


@admin.register(DPP)
class DPPAdmin(admin.ModelAdmin):
    list_display = ('student', 'category', 'amount', 'is_paid')
    list_filter = ('category', 'is_paid')


@admin.register(PaymentReminder)
class PaymentReminderAdmin(admin.ModelAdmin):
    list_display = ('student', 'reminder_type', 'sent_at', 'is_read')
    list_filter = ('reminder_type', 'is_read')


@admin.register(SPPReport)
class SPPReportAdmin(admin.ModelAdmin):
    list_display = ('grade', 'month', 'year', 'status', 'total_collected', 'reviewed_by')
    list_filter = ('status', 'grade')


@admin.register(DPPReport)
class DPPReportAdmin(admin.ModelAdmin):
    list_display = ('grade', 'category', 'status', 'total_collected')
    list_filter = ('status', 'category')


@admin.register(Compensation)
class CompensationAdmin(admin.ModelAdmin):
    list_display = ('student', 'comp_type', 'original_amount', 'comp_amount', 'final_amount', 'is_active')
    list_filter = ('comp_type', 'is_active')
