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

    def _test_cfps(self):
        '''sem2017A = Semester.objects.create(
            year=2019,
            semester="A"
        )'''

        pacific = pytz.timezone('US/Pacific')
        dt_pacific_now = datetime.now(tz=pacific)

        sem2017A = Semester.objects.get(year=2017, semester="A")

        print("Test cfp sem2017A type is:", type(sem2017A))
        print("Test cfp sem2017A is:", sem2017A)
        print("Test cfp sem2017A year is:", sem2017A.year)
        test_user = get_user_model().objects.get(email='testuser3@lbto.org', partner='AZ')

        print("Test cfp user type is:", type(test_user))
        print("Test cfp user id is:", test_user.id)
        print("Test cfp user is:", test_user)
        cfp2 = CfP.objects.get(semester=sem2017A, pi=test_user)
        print("Test cfp2 open_cfp is:", cfp2.open_cfp)
        cfp3 = CfP.objects.filter(pi=test_user, semester=sem2017A)
        print("cfp3 queryset:", str(cfp3.query))
        print("cfp3", cfp3)
        #print("Test cfp open_cfp is:", type(cfp3[0].open_cfp.astimezone(tz=pytz.timezone(cfp3[0].open_cfp_tz))))
        print("Test cfp open_cfp type is:", type(cfp3[0].open_cfp.astimezone(tz=pytz.timezone('US/Pacific'))))
        print("Test cfp open_cfp is:", cfp3[0].open_cfp.astimezone(tz=pytz.timezone('US/Pacific')))

    def handle(self, *args, **options):
        self._test_cfps()
