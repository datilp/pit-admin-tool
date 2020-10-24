from rest_framework import routers
from django.urls import path, include  # allows to create paths within our app
from .views import CfPCurrentSemView, CfPViewSet, SemesterViewSet

#from django.urls import get_resolver, reverse
#print(get_resolver().reverse_dict.keys())
#https://www.django-rest-framework.org/api-guide/routers/
# shows all the possible urls the application has, for cfpView-details
#  docker-compose run --rm pit_admin_app sh -c "python manage.py show_urls"

router = routers.DefaultRouter()
router.register(r'api/cfp/', CfPViewSet, 'cfpView')
router.register(r'api/semester', SemesterViewSet, 'cfpSemester')

urlpatterns = router.urls
urlpatterns.append(
    path(r'api/current_sem/', CfPCurrentSemView.as_view(), name='cfp_current_sem'),
)
