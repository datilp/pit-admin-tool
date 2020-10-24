from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

# The models file contains the fields and behaviors of your data.
# Usually it maps to a table in the database.
# We are not using the models.User or the models.UserManager but our own
# as we are doing some changes to it.
# Specifically we are setting the email to be the username
# and we are adding partner choices and attribute to the user attributes.
# https://docs.djangoproject.com/en/3.0/ref/contrib/auth/


class UserManager(BaseUserManager):
    """password default to None in case we want to create a non active
       user. """

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError("Users must have an email address")

        """with email normalized, i.e. lowercase in the hostname part"""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # set_password here will encrypt the password
        #print("partner is:", user.partner)
        #print("password is:", password)
        # TODO when password gets here is already NONE, cause we don't save the
        #   password wih the user, but where is it saved if it is saved and how
        user.set_password(password)
        user.save(using=self._db)
        """https://stackoverflow.com/questions/57667334/what-is-the-value-of-self-db-by-default-in-django
           using=self._db is to remind me I can point to another database.
           self._db is set to None by default and that makes the code to
           use the "DEFAULT" database as set in settings.py.
           However if we have another database and we want to use it, we do
           using="my_new_database"
           in settings.py
           'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'HOST': os.environ.get('DB_HOST'),
              ... },
           'my_new_database' : { ... }
           }  """

        return user

    def create_superuser(self, email, password=None):
        """Creates and saves a super user"""
        user = self.create_user(email, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user

    #def get_by_natural_key(self, username):
    #    print("get_by_natural_key user")
    #    return self.get(**{self.model.USERNAME_FIELD: username})

# create our User model
# This model inherits the AbstractBaseUser
# Very important! in settings.py I set the AUTH_USER_MODEL
# config param to this user model.
# E.g.
# AUTH_USER_MODEL = 'core.User'
# So whenever in the code I use django.contrib.auth get_user_model()
# I get the one I set in AUTH_USER_MODEL.
class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that uses email as username and
       and adds a choice of partners to the partner attribute"""

    """
       I think I could have use the class Meta: to override some 
       model internals such as the table name this object is
       represented in the database
       class Meta:
         db_table = "my_user"
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    PARTNER_LIST = (
        ('AIP', 'AIP'),
        ('AZ', 'University of Arizona'),
        ('INAF', 'INAF'),
        ('MPIA', 'MPIA'),
        ('NM', 'Notre Dam'),
        ('OS', 'Ohio State University'),
        ('UM', 'University of Minnesota'),
        ('UV', 'University of Virginia'),
    )
    partner = models.CharField(max_length=4, choices=PARTNER_LIST)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
