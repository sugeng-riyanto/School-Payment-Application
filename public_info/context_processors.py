from .models import SchoolProfile


def school_profile(request):
    profile = SchoolProfile.get_profile()
    ctx = {'school': profile}
    if request.user.is_authenticated and request.user.role == 'parent':
        students = request.user.children.all()
        if students:
            from payments.models import BlastEmailLog
            ctx['unread_blast_count'] = BlastEmailLog.objects.filter(student__in=students, is_read=False).count()
    return ctx
