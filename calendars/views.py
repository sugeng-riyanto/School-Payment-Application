from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AcademicCalendar


@login_required
def calendar_list(request):
    calendars = AcademicCalendar.objects.all()
    # Check if there's a recent update alert (within last 7 days)
    from django.utils import timezone
    from datetime import timedelta
    recent_update = calendars.filter(updated_at__gte=timezone.now() - timedelta(days=7)).first()
    return render(request, 'calendars/calendar_list.html', {
        'calendars': calendars,
        'recent_update': recent_update,
    })


@login_required
def upload_calendar(request):
    if request.user.role not in ['admin', 'tu', 'vp_activity']:
        messages.error(request, 'Akses ditolak.')
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')
        description = request.POST.get('description', '')
        update_notes = request.POST.get('update_notes', '')
        if not title or not file:
            messages.error(request, 'Judul dan file wajib diisi.')
            return render(request, 'calendars/upload_calendar.html')
        AcademicCalendar.objects.create(
            title=title, file=file, description=description,
            update_notes=update_notes, uploaded_by=request.user,
        )
        messages.success(request, 'Kalender akademik berhasil diupload.')
        return redirect('calendars:list')
    return render(request, 'calendars/upload_calendar.html')


@login_required
def edit_calendar(request, pk):
    calendar = get_object_or_404(AcademicCalendar, id=pk)
    if request.user.role not in ['admin', 'tu', 'vp_activity']:
        messages.error(request, 'Akses ditolak.')
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        calendar.title = request.POST.get('title', calendar.title)
        calendar.description = request.POST.get('description', '')
        calendar.update_notes = request.POST.get('update_notes', '')
        if request.FILES.get('file'):
            calendar.file = request.FILES['file']
        calendar.save()
        messages.success(request, f'Kalender akademik diupdate: {calendar.update_notes}')
        return redirect('calendars:list')
    return render(request, 'calendars/upload_calendar.html', {'calendar': calendar, 'editing': True})
