from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    ''' Set up function, sets things up before tests run'''
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@gmail.com',
            password='password123'
        )
        """ use the client to log the user in
            instead of having to code it ourselves"""
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password="password123",
            name="Test user full name",
            partner="AZ"
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        """ generates the urls to that feature """
        url = reverse('admin:core_user_changelist')
        """ uses the test client to do a http request on the url"""
        res = self.client.get(url)
        #print("response content:", res.content)
        #print("partner:", self.user.get_partner_display())
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.get_partner_display())

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        """ e.g. url generated will be like /admin/core/user/432 """
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
