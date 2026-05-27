from .models import SchoolProfile
from accounts.models import AcademicYear


def school_profile(request):
    profile = SchoolProfile.get_profile()
    ctx = {'school': profile}

    if request.user.is_authenticated:
        from accounts.models import AcademicYear
        years = AcademicYear.objects.all().order_by('-start_date')
        ctx['academic_years'] = years

        active = None
        year_id = request.session.get('academic_year_id')
        if year_id:
            active = AcademicYear.objects.filter(id=year_id).first()
        if not active:
            active = AcademicYear.objects.filter(is_active=True).first()
        if not active and years:
            active = years.first()
        ctx['active_academic_year'] = active

        if request.user.role == 'parent':
            students = request.user.children.all()
            if students:
                from payments.models import BlastEmailLog
                ctx['unread_blast_count'] = BlastEmailLog.objects.filter(student__in=students, is_read=False).count()

    return ctx
