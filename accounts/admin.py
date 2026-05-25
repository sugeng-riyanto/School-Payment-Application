from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, AcademicYear, Grade, ClassGrade, Student


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'assigned_level', 'phone', 'alamat', 'avatar')}),
    )


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'start_date', 'end_date')


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')


@admin.register(ClassGrade)
class ClassGradeAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'academic_year')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'nisn', 'nis', 'parent', 'class_grade', 'is_active')
    list_filter = ('is_active', 'class_grade__grade')
    search_fields = ('full_name', 'nis', 'nisn')
