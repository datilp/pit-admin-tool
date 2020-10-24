from django.core.management.base import BaseCommand
from datetime import datetime
import pytz
from CfP_app.models import CfP, Semester
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'some help'

    def test_user(self, email, password, **extra_fields):
        """Create a test user"""
        return get_user_model().objects.create_user(email, password, **extra_fields)

    def _create_cfps(self):
        '''sem2017A = Semester.objects.create(
            year=2019,
            semester="A"
        )'''

        pacific = pytz.timezone('US/Pacific')
        dt_pacific = datetime.strptime("2020-09-16 23:29:35.884703Z", "%Y-%m-%d %H:%M:%S.%f%z").\
            astimezone(tz=pacific)

        sem2017A = Semester(year=2017, semester="A")
        sem2017A.save()

        #test_user = self.test_user(email='testuser3@lbto.org', password='abcd123', partner='AZ')
        test_user = get_user_model().objects.get(email='testuser3@lbto.org', partner='AZ')

        cfp1 = CfP(semester=sem2017A,
                   pi=test_user,
                   open_cfp=dt_pacific,
                   open_cfp_tz=dt_pacific.tzname())
        cfp1.save()
        '''cfp_object = CfP.objects.create(
            semester=sem2017B,
            pi=test_user,
            open_cfp=dt_pacific_now,
            open_cfp_tz=dt_pacific_now.tzname()
        )'''

    def handle(self, *args, **options):
        self._create_cfps()
