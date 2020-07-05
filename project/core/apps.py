from django.apps import AppConfig

# I created a core application just to keep the admin form and
# the customized user model separate.
# Very important! in settings.py I set the AUTH_USER_MODEL
# config param to this user model.
# E.g.
# So whenever in the code I use django.contrib.auth get_user_model()
# I get the one I set in AUTH_USER_MODEL.
# AUTH_USER_MODEL = 'core.User'


class CoreConfig(AppConfig):
    name = 'core'
