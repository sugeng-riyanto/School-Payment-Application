from django.db import models
from accounts.models import User


class AcademicCalendar(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='academic_calendars/', help_text='PDF file')
    is_active = models.BooleanField(default=True)
    update_notes = models.TextField(blank=True, help_text='Catatan perubahan')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='calendar_uploads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Academic Calendar'
        verbose_name_plural = 'Academic Calendars'
        ordering = ['-updated_at']

    def __str__(self):
        return self.title
