from django.contrib import admin
from .models import ECAType, ECAProgram, ECARegistration, ECAPayment, ECAScore, ECAReport


@admin.register(ECAType)
class ECATypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')


@admin.register(ECAProgram)
class ECAProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'eca_type', 'grade', 'price', 'duration', 'is_open')
    list_filter = ('is_open', 'grade', 'eca_type')


@admin.register(ECARegistration)
class ECARegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'program', 'status', 'is_paid', 'registered_at')
    list_filter = ('status', 'is_paid')


@admin.register(ECAPayment)
class ECAPaymentAdmin(admin.ModelAdmin):
    list_display = ('registration', 'amount', 'is_paid', 'paid_at')


@admin.register(ECAScore)
class ECAScoreAdmin(admin.ModelAdmin):
    list_display = ('student', 'program', 'score', 'scored_at')
    list_filter = ('program',)


@admin.register(ECAReport)
class ECAReportAdmin(admin.ModelAdmin):
    list_display = ('program', 'period', 'status', 'total_revenue', 'reviewed_by')
    list_filter = ('status', 'period')
