from django.core.exceptions import ObjectDoesNotExist
from rest_framework.test import APITestCase as TestCase
from rest_framework import status  # module containing status codes in
from CfP_app.models import Semester, CfP
import base64
from datetime import datetime
from django.urls import reverse
from django.contrib.auth import get_user_model
import pytz
from dateutil.parser import parse
import json
from django.db import models


def shift_paths(exclude, name):
    return tuple(item.split('.', 1)[1] for item in exclude
                 if item.startswith(('{0}.'.format(name), '*.')))


# Create a test user
def test_user(email='testuser@lbto.org', password='abcd123', **extra_fields):
    """Create a test user"""
    return get_user_model().objects.create_user(email, password, **extra_fields)


def get_basic_auth_header(username, password):
    return 'Basic %s' % base64.b64encode(
        ('%s:%s' % (username, password)).encode('ascii')).decode()


class ModelTest(TestCase):

    ''' setUp function sets things up for all the tests '''
    def setUp(self):
        self.email = 'testuser@lbto.org'
        self.password = 'abcd123'
        self.partner = 'AZ'
        az_user = test_user(email='testuser@lbto.org', password='abcd123', partner='AZ')
        it_user = test_user(email='test@inaf.it', password='abcd123', name='Pepe Grillo', partner='INAF')

        self.it_user = it_user
        self.user = az_user


        login_url = reverse('user:knox_login')

        # setting credentials works the same as setting the header
        # Note: Watch out that if BasicAuthentication is one of the
        # DEFAULT_AUTHENTICATION_CLASSES options in settings.py and
        # the HTTP_AUTHORIZATION is set with the
        #self.client.credentials(
        #    HTTP_AUTHORIZATION=get_basic_auth_header(self.email, self.password)
        #)
        #res = self.client.post(login_url, {}, format='json')

        header = {'HTTP_AUTHORIZATION': get_basic_auth_header(self.email, self.password)}
        res = self.client.post(login_url, {}, format='json', **header)

        #print("response:", res.data)
        #'''
        self.assertEqual(res.status_code, 200)
        self.assertIn('token', res.data)
        username_field = self.user.USERNAME_FIELD
        self.assertNotIn(username_field, res.data)
        #'''

        self.token = res.data['token']
        #print("Token:", self.token, "[end]")

        self.sem2016B = Semester.objects.create(
            year=2016,
            sem="B"
        )

        self.sem2017A = Semester.objects.create(
            year=2017,
            sem="A"
        )

        self.tz = pytz.timezone('America/Phoenix')
        self.cfp1 = CfP.objects.create(
            semester=self.sem2016B,
            pi=az_user,
            open=datetime.now(tz=self.tz),
            tz=self.tz
        )

        self.cfp2 = CfP.objects.create(
            semester=self.sem2017A,
            pi=az_user,
            open=datetime.now(tz=self.tz),
            tz=self.tz
        )

        self.cfp2 = CfP.objects.create(
            semester=self.sem2017A,
            pi=it_user,
            open=datetime.now(tz=self.tz),
            tz=self.tz
        )

    def test_semester_str(self):
        """Test a semester representation"""
        #print("test_semester_str")
        semester = Semester.objects.create(
            year=2019,
            sem="B"
        )

        self.assertEquals(str(semester), "2019B")

    def test_create_CfP(self):
        """Test creation of CfP object"""
        sem2019B = Semester.objects.create(
            year=2019,
            sem="B"
        )

        az_user = test_user(email='testuser2@lbto.org', password='abcd123', partner='AZ')
        pacific = pytz.timezone('US/Pacific')
        dt_pacific_now = datetime.now(tz=pacific)
        #with self.assertRaises(ValueError):
        cfp_object = CfP.objects.create(
                semester=sem2019B,
                pi=az_user,
                open=dt_pacific_now,
                tz=dt_pacific_now.tzname()

            )
        header = {'HTTP_AUTHORIZATION': "token " + self.token}
        #print(cfp_object.pi.partner)
        #print(az_user.CfP_entry.all())
        self.assertEquals(cfp_object.pi.id, az_user.id)
        self.assertEquals(cfp_object.pi.email, 'testuser2@lbto.org')
        self.assertEquals(cfp_object.open, dt_pacific_now)
        self.assertEquals(cfp_object.tz, dt_pacific_now.tzname())
        self.assertEquals(cfp_object.close, None)

    def test_CfP_list_url(self):
        """Test what CfPs login user has"""
        #from django.urls import get_resolver, reverse
        #print(get_resolver().reverse_dict.keys())
        #https://www.django-rest-framework.org/api-guide/routers/
        header = {'HTTP_AUTHORIZATION': "token " + self.token}
        url = reverse('cfpView-list')
        res = self.client.get(url, **header)

        # check status code is OK
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # should return two items
        # print(json.dumps(res.data, indent=2))
        self.assertEqual(len(res.data), 2)
        # test the user id is same as the user we logged as in
        self.assertEqual(res.data[0]['pi']['id'], self.user.id)
        self.assertEqual(0, 0)

    def test_fail_CfP_list_url(self):
        """Test failed authorization on CfPs login user query"""
        #from django.urls import get_resolver, reverse
        #print(get_resolver().reverse_dict.keys())
        #https://www.django-rest-framework.org/api-guide/routers/
        header = {}
        url = reverse('cfpView-list')
        res = self.client.get(url, **header)

        # check status code is OK
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_CfP_url_with_id_query_param(self):
        """Test CfP list contents for a given filter"""
        #{"id": 4, "open": "2020-07-11T23:27:13.762819Z", "close": null, "semester": 4, "pi": 3}
        header = {'HTTP_AUTHORIZATION': "token " + self.token}
        url = reverse('cfpView-list')
        #print("id is ", self.cfp1.id)
        # in CfP_app/views.py/CfPViewSet/get_queryset method I check
        # for request parameter cfp_id
        payload = {'id': self.cfp1.id}
        res = self.client.get(url,
                              payload,
                              **header)
        # check status code is OK
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # should return one item
        self.assertEqual(len(res.data), 1)
        # test the user id is same as the user we logged as in
        self.assertEqual(res.data[0]['pi']['id'], self.user.id)

    def test_list_CfP_url_with_query_param(self):
        """Test CfP list contents for a given filter"""
        #{"id": 4, "open": "2020-07-11T23:27:13.762819Z", "close": null, "semester": 4, "pi": 3}
        header = {'HTTP_AUTHORIZATION': "token " + self.token}
        url = reverse('cfpView-list')
        # in CfP_app/views.py/CfPViewSet/get_queryset method check for query handling
        payload = {'semester': self.sem2017A.id,
                   'pi': self.user.id}
        res = self.client.get(url,
                              payload,
                              **header)
        # check status code is OK
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # should return one item
        self.assertEqual(len(res.data), 1)
        # test the user id is same as the user we logged as in
        self.assertEqual(res.data[0]['semester']['id'], payload['semester'])
        self.assertEqual(res.data[0]['pi']['id'], payload['pi'])

    def test_CfP_current_sem_with_partner_query_param(self):
        """Test json query for web app, with currentSem"""
        #{"id": 4, "open": "2020-07-11T23:27:13.762819Z", "close": null, "semester": 4, "pi": 3}
        # this doesn't work use credentials below
        #header = {'HTTP_AUTHORIZATION': "Token %s" % self.token}
        self.client.credentials(HTTP_AUTHORIZATION=('Token %s' % self.token))
        header = {}
        url = reverse('cfp_current_sem')
        #print("url:", url)

        # in CfP_app/views.py/CfPViewSet/get_queryset method check for query handling
        payload = {'pi__partner': "AZ"}
        res = self.client.get(url,
                              payload,
                              **header)
        #print(json.dumps(res.data, indent=2))
        # check status code is OK
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # should return one item
        self.assertEqual(len(res.data['semList']), 2)
        # test the user id is same as the user we logged as in
        self.assertTrue(str(res.data['currentSem']['semester']['id']).isnumeric())
        self.assertEqual(res.data['semList'][0]['pi']['id'], self.user.id)

    # create a new CfP
    def test_create_CfP_url(self):
        """Test CfP create a new CfP via the url api
           There are several tests here:
           We create a new CfP using semester id and pi id
           and also using it's keys by semester year and sem
        """
        """The url should be the same, the difference is the http method
        If we use POST it should call the create action.
        https://www.django-rest-framework.org/api-guide/routers/
        """
        #header = {'HTTP_AUTHORIZATION': "token " + self.token}
        self.client.credentials(HTTP_AUTHORIZATION=('Token %s' % self.token))
        header = {}
        url_create = reverse('cfpView-list')

        #print("test_create_CfP_url:[%s]" % url_create)
        sem2017B = Semester.objects.create(
            year=2017,
            sem="B"
        )

        #open_time = datetime.now(tz=self.tz)
        pacific = pytz.timezone('US/Pacific')
        open_time = datetime.strptime("2020-09-16 23:29:35.884703Z", "%Y-%m-%d %H:%M:%S.%f%z"). \
            astimezone(tz=pacific)
        # open_time = datetime.now(tz=pytz.utc)
        #print("id is ", self.cfp1.id)
        # in CfP_app/views.py CfPViewSet.get_queryset method I check
        # for request parameter cfp_id
        #print("user id is ", self.user.id)
        payload_create = {'semester_id': sem2017B.id,
                          # since we are authenticating with the user token
                          # we don't need to specify the user id
                          'pi_id': self.user.id,
                          'open': open_time,
                          'tz': str(open_time.tzinfo)}

        res = self.client.post(url_create,
                               payload_create,
                               **header)

        #print(json.dumps(res.data, indent=2))
        #print("Response error:", res.reason_phrase)
        # 201 a resource has been created successfully
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['semester']['year'], sem2017B.year)
        self.assertEqual(res.data['semester']['sem'], sem2017B.sem)
        # user should be the user passed in
        self.assertEqual(res.data['pi']['id'], payload_create['pi_id'])
        self.assertEqual(str(datetime.strptime(res.data['open'], "%Y-%m-%dT%H:%M:%S.%fZ")
                             .astimezone(tz=pytz.timezone(res.data['tz']))), str(payload_create['open']))

        # Query back based on the new semester and user
        #res = self.client.get(url, {'semester': sem2020B.id,
        #                            'pi': self.user.id}, **header)
        #res = self.client.get(url, {'semester': sem2017B.id}, **header)
        # These two payload produce the same results
        # payload = {
        #     'semester': sem2017B.id,
        #     'pi': self.user.id
        # }
        payload = {
            'semester__year': sem2017B.year,
            'semester__sem': sem2017B.sem,
            'pi__email': self.user.email
        }
        url_get = reverse('cfp_current_sem')
        res = self.client.get(url_get, payload, **header)
        #print(json.dumps(res.data, indent=2))
        # check status code is OK
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # should return one item
        self.assertEqual(len(res.data['semList']), 1)
        # semester should be the new semester
        self.assertEqual(res.data['semList'][0]['semester']['id'], payload_create['semester_id'])
        # user should be the user passed in
        self.assertEqual(res.data['semList'][0]['pi']['id'], payload_create['pi_id'])
        self.assertEqual(str(datetime.strptime(res.data['semList'][0]['open'], "%Y-%m-%dT%H:%M:%S.%fZ")
                         .astimezone(tz=pytz.timezone(res.data['semList'][0]['tz']))), str(payload_create['open']))

        """ Using semester year and sem"""
        payload_create = {'semester__year': 2022,
                          'semester__sem': "A",
                          # since we are authenticating with the user token
                          # we don't need to specify the user id
                          'pi_id': self.user.id,
                          'open': open_time,
                          'tz': str(open_time.tzinfo)}

        res = self.client.post(url_create,
                               payload_create,
                               **header)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # should return one item
        #print(json.dumps(res.data, indent=2))
        # semester should be the new semester
        self.assertEqual(res.data['semester']['year'], payload_create['semester__year'])
        self.assertEqual(res.data['semester']['sem'], payload_create['semester__sem'])
        # user should be the user passed in
        self.assertEqual(res.data['pi']['id'], payload_create['pi_id'])
        self.assertEqual(str(datetime.strptime(res.data['open'], "%Y-%m-%dT%H:%M:%S.%fZ")
                             .astimezone(tz=pytz.timezone(res.data['tz']))), str(payload_create['open']))

    # update/modify/patch an existing entry
    def test_modify_CfP_url(self):
        """Test CfP create a new CfP"""
        """The url should be the same, the difference is the http method
        If we use POST it should call the create action.
        https://www.django-rest-framework.org/api-guide/routers/
        """
        #header = {}
        header = {'HTTP_AUTHORIZATION': "token " + self.token}

        # url = reverse('cfpView-list')
        # in a ModelViewSet <something>-detail typically means you are passing
        # some sort of primary index.
        #  docker-compose run --rm pit_admin_app sh -c "python manage.py show_urls"
        # shows all the possible urls the application has, for cfpView-details
        # we have rest url /api/cfp//P<pk>.<format>
        # that P<pk> is the primary key and we pass that in the "args" parameter in
        # the reverse function as a tuple.
        #

        patch_url = reverse('cfpView-detail',  args=(self.cfp1.id,))
        # cfp1 has a semester 2016B, lets replace it with a new semester
        # and new close dates and time zone.
        sem2017B = Semester.objects.create(
            year=2017,
            sem="B"
        )

        # in CfP_app/views.py CfPViewSet.get_queryset method I check
        # for request parameter cfp_id
        # utctime = datetime.now(pytz.utc)
        # phoenix = pytz.timezone('America/Phoenix')
        # phoenixtime = datetime.now(phoenix)
        ushawaiitime = datetime.now(tz=pytz.timezone('US/Hawaii'))
        # print("Rome time:", str(datetime.strptime("2020-10-11T00:00:00.0+02:00", "%Y-%m-%dT%H:%M:%S.%f%z")))
        # print("Rome time:", datetime.strptime("2020-10-11T00:00:00.0+02:00", "%Y-%m-%dT%H:%M:%S.%f%z").
        #       astimezone(tz=pytz.utc))
        # print("Rome timeZ:", datetime.strptime("2020-10-11T00:00:00.0Z", "%Y-%m-%dT%H:%M:%S.%fZ").
        #       astimezone(tz=pytz.timezone('Europe/Rome')))
        # print("utctime:", utctime)
        # print("phoenix time:", phoenixtime)
        # print("hawaii time:", ushawaiitime)
        # print("hawaii time to utc:", ushawaiitime.astimezone(tz=pytz.utc))
        # print("hawaii time str:", str(ushawaiitime))
        # print("hawaii tz:", ushawaiitime.tzname())
        # print("hawaii tz:", ushawaiitime.tzinfo)
        # print("utc to phoenix", utctime.astimezone(phoenix))

        # IMPORTANT NOTE:
        # unfortunately the Time Zone is not saved in the django DateTimeField, so we are saving in a
        # separate column the tz timezone field.
        # no need to do the json conversion as I did above, django does it for you

        #print("Patch url###:", patch_url)
        payload = {'semester_id': sem2017B.id,
                   'close': ushawaiitime,
                   'tz': ushawaiitime.tzinfo}

        res = self.client.patch(patch_url,
                                payload,
                                **header)

        #print("Patch res:", json.dumps(res.data, indent=2))
        # print("Patch error msg:", res.reason_phrase)
        # Test the patch output
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['semester']['id'], payload['semester_id'])
        self.assertNotEqual(res.data['close'], str(payload['close']))
        self.assertEqual(parse(res.data['close']).
                         astimezone(tz=pytz.timezone(res.data['tz'])),
                         payload['close'])
        self.assertEqual(res.data['tz'], payload['tz'].tzname(None))
        self.assertEqual(res.data['tz'], str(payload['tz']))
        # user should be the user passed in
        self.assertEqual(res.data['pi']['id'], self.user.id)

        # Do the same test from a get query
        payload_get = {'semester': sem2017B.id,
                       'pi': self.user.id}
        # Query back based on the new semester and user
        url = reverse('cfp_current_sem')
        res = self.client.get(url,
                              payload_get,
                              **header)

        # check status code is OK
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['semList']), 1)
        # semester should be the new semester
        self.assertEqual(res.data['semList'][0]['semester']['id'], payload['semester_id'])
        # The following should not be equal as the date save in the database by python/django
        # doesn't contain timezone information. Hence it should not match
        self.assertNotEqual(res.data['semList'][0]['close'], str(payload['close']))
        # We use dateutil parser to easily parse the date, then we apply the timezone
        # which we compare to the original one and these should match.
        self.assertEqual(parse(res.data['semList'][0]['close']).
                         astimezone(tz=pytz.timezone(res.data['semList'][0]['tz'])),
                         payload['close'])

        # The next are two versions of the same thing
        # Note the tzname(None) to get the actual geographical zone as oppose to the DST
        # shorthand.
        # str is basically the same. You can look at the class timezone(tzinfo) in datetime.py
        # where str is tzname(None)
        #self.assertEqual(res.data[0]['tz'], ushawaiitime.tzinfo.tzname(None))
        self.assertEqual(res.data['semList'][0]['tz'], payload['tz'].tzname(None))
        self.assertEqual(res.data['semList'][0]['tz'], str(payload['tz']))
        # user should be the user passed in
        self.assertEqual(res.data['semList'][0]['pi']['id'], self.user.id)

    def test_list_CfP_url_with_query_param(self):
        """Test CfP list contents for a given filter"""
        #{"id": 4, "open": "2020-07-11T23:27:13.762819Z", "close": null, "semester": 4, "pi": 3}
        header = {'HTTP_AUTHORIZATION': "token " + self.token}
        url = reverse('cfpView-list')
        # in CfP_app/views.py/CfPViewSet/get_queryset method check for query handling
        payload = {  # 'semester': self.sem2017A.id,
                     'semester__year': self.sem2017A.year,
                     'semester__sem': self.sem2017A.sem,
                     'pi__partner': "AZ"}
        res = self.client.get(url,
                              payload,
                              **header)
        #print(json.dumps(res.data, indent=2))
        # check status code is OK
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # should return one item
        self.assertEqual(len(res.data), 1)

        # test the user id is same as the user we logged as in
        self.assertEqual(res.data[0]['semester']['year'], payload['semester__year'])
        self.assertEqual(res.data[0]['semester']['sem'], payload['semester__sem'])
        self.assertEqual(res.data[0]['pi']['id'], self.user.id)

    # In this test I tried to get the json output you'd normally get via a http request.
    # However, even though I get a json output. The json doesn't have the fields for the foreign
    # fields as it does the http response.
    def ntest_query_CfP_model(self):
        """Query CfP model"""
        """Query on foreign fields and return foreign object fields in 
        queryset. 
        """

        '''
        Making queries via the django model
        https://docs.djangoproject.com/en/3.1/topics/db/queries/
        Making raw SQL queries
        https://docs.djangoproject.com/en/3.1/topics/db/sql/

        '''
        # Querying on semester: year and semester
        #cfp_objs = CfP.objects.filter(semester=5)
        cfp_objs = CfP.objects.filter(semester__year=2017, semester__sem="A")
        print("cfps with sem 2017A: ", cfp_objs.count())
        import json
        from django.core import serializers
        from CfP_app.serializers import CfPSerializer
        #print("cfps with sem 2017A: ", CfPSerializer.serialize('json', cfp_objs,
        print("cfps with sem 2017A: ", serializers.serialize('json', cfp_objs,
                                                             indent=2,
                                                             use_natural_foreign_keys=False,
                                                             use_natural_primary_keys=False))
        # from django.http import JsonResponse
        # print("2 cfps with sem 2017A: ", JsonResponse(cfp_objs[0], safe=False))

        # from json import dumps, loads, JSONEncoder
        # print ("####", loads(serializers.serialize('json', cfp_objs)))
        # django profiling debugging
        # https://stackoverflow.com/questions/17531598/profiling-django-views-line-by-line
        # print("cfps with sem 2017A: ", serializers.serialize('json', cfp_objs,
        #                                                     indent=2))
        # OK https://stackoverflow.com/questions/18146905/django-convert-queryset-with-related-objects-to-json
        # print("cfps with sem 2017A: ", cfp_objs.values("semester__year", "semester__sem", "open",
        #                                               "close", "pi", "pi__name", "pi__partner"))
        # KO print("cfps with sem 2017A: ", self.model_to_dict(cfp_objs[0]))
        # print("cfps with sem 2017A: ", deep_dump_instance(cfp_objs))
        self.assertEqual(cfp_objs.count(), 2)

        # Querying on PI partnership
        cfp_objs = CfP.objects.filter(pi__partner="INAF")
        print("cfps with partner INAF: ", cfp_objs.count())
        self.assertEqual(cfp_objs.get().semester.year, 2017)
        self.assertEqual(cfp_objs[0].semester.year, 2017)
        self.assertEqual(cfp_objs.count(), 1)

