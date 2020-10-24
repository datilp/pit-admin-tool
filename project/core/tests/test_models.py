from django.test import TestCase
from django.contrib.auth import get_user_model
''' we use get_user_model instead of importing the user model directly
    later on if we change the user model by using get_user_model we only
    have to change the configuration
'''


class ModelTest(TestCase):

    def test_create_user_with_email_sucessful(self):
        """Test creating a new user with an email is successful"""
        email = 'isuarezsola@gmail.com'
        password = 'Testpass123'
        partner = 'AZ'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            partner="AZ"
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.partner, partner)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized"""
        email = 'isuarezsola@GMAIL.COM'
        user = get_user_model().objects.create_user(email, "test123", **{'partner': "AZ"})
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test created user without email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test123", **{'partner': "AZ"})

    def test_create_new_super_user(self):
        """Test create super user"""
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
