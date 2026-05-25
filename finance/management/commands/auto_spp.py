from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from accounts.models import Student, AcademicYear
from finance.models import SPP, SPPBill, PaymentReminder


class Command(BaseCommand):
    help = 'Auto-generate SPP bills on 1st of month + send reminders on 10th/20th/1month overdue'

    def handle(self, *args, **options):
        today = date.today()
        academic_year = AcademicYear.objects.filter(is_active=True).first()
        if not academic_year:
            self.stdout.write('No active academic year found.')
            return

        if today.day == 1:
            self._generate_bills(today, academic_year)

        self._send_reminders(today, academic_year)
        self.stdout.write('Done.')

    def _generate_bills(self, today, academic_year):
        students = Student.objects.filter(is_active=True, class_grade__academic_year=academic_year)
        month = today.month
        year = today.year
        created = 0
        for student in students:
            if not student.class_grade:
                continue
            spp_rate = SPP.objects.filter(
                academic_year=academic_year,
                grade=student.class_grade.grade,
                is_active=True
            ).first()
            if spp_rate:
                _, was_created = SPPBill.objects.get_or_create(
                    student=student,
                    month=month,
                    year=year,
                    defaults={
                        'spp': spp_rate,
                        'amount': spp_rate.amount,
                        'due_date': date(year, month, 10),
                    }
                )
                if was_created:
                    created += 1
        self.stdout.write(f'Created {created} SPP bills for {month}/{year}.')

    def _send_reminders(self, today, academic_year):
        unpaid = SPPBill.objects.filter(is_paid=False)
        reminders_sent = 0

        for bill in unpaid:
            bill_date = date(bill.year, bill.month, 1)
            days_overdue = (today - bill_date).days

            if days_overdue >= 31:
                rtype = 3
            elif today.day >= 20 and days_overdue < 31:
                rtype = 2
            elif today.day >= 10:
                rtype = 1
            else:
                continue

            exists = PaymentReminder.objects.filter(
                spp_bill=bill, reminder_type=rtype,
                sent_at__date=today
            ).exists()
            if not exists:
                PaymentReminder.objects.create(
                    spp_bill=bill,
                    student=bill.student,
                    reminder_type=rtype,
                    academic_year=academic_year,
                    month=bill.month,
                )
                reminders_sent += 1

        self.stdout.write(f'Sent {reminders_sent} reminders.')
