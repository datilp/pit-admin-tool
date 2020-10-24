import json
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from CfP_app.models import Semester
from .serializers import SemesterSerializer, CfPSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, exceptions  # module containing status codes in
from knox.auth import TokenAuthentication

'''
# Lead Viewset
class LeadViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = LeadSerializer

    def get_queryset(self):
        return self.request.user.leads.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
'''


class SemesterViewSet(viewsets.ModelViewSet):
    # permission_classes = [
    #    permissions.IsAuthenticated,
    # ]
    serializer_class = SemesterSerializer

class CfPCurrentSemView(APIView):
    """
    Specific view that returns a json structure with a list
    of CfP for the given query headed by the CfP for the current
    semester if available. If not available it will create one
    by default.
    """
    # no need for this as in settings.py we are already
    # specifying it in the DEFAULT_AUTHENTICATION_CLASSES
    # authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request):
        """
        :param request:
        :param format:
        :return:
        """
        from datetime import datetime
        date = datetime.now()

        # workout current semester. If month is between July and December
        # we assume next year semester
        (year, sem) = (date.year + 1, "A") if 7 < date.month < 12 \
            else (date.year, "B")
        try:
            semester = Semester.objects.get(year=year,
                                            sem=sem)
        except ObjectDoesNotExist:
            semester = Semester.objects.create(year=year,
                                               sem=sem)

        # get the cfp list as per cfp view set and then add the current semester info
        #data = CfPViewSet.as_view('get': 'list')(request._request).data
        # https://stackoverflow.com/questions/51149599/call-viewset-method-from-another-view
        resp = CfPViewSet.as_view({'get': 'list'})(request._request)
        new_current_sem = {'idx': len(resp.data),
                           'semester': {'id': semester.id, 'year': year, 'sem': sem},
                           'open': None,
                           'close': None,
                           'tz': None,
                           'pi': {'id': request.user.id}}

        #print("New current sem", json.dumps(new_current_sem, indent=2))
        #print(json.dumps(resp.data, indent=2))

        current_cfp = next(((idx, x) for idx, x in enumerate(resp.data)
                            if x['semester']['id'] == semester.id),
                           (-1 if len(resp.data) == 0 else len(resp.data), new_current_sem))
        current_cfp[1]['idx'] = current_cfp[0]
        #print("Query show current_cfp:", json.dumps(current_cfp, indent=2))
        resp.data = {
            'currentSem': current_cfp[1],
            'semList': resp.data
        }
        #print("resp.data:", json.dumps(resp.data, indent=2))

        return Response(resp.data)


class CfPViewSet(viewsets.ModelViewSet):
    # no need for this as in settings.py we are already
    # specifying it in the DEFAULT_AUTHENTICATION_CLASSES
    # authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = CfPSerializer

    def create(self, request, **kwargs):
        #print("in CfPViewSet create method")
        # if instead of a semester_id we get the semester data then dealt with
        # that case here. Find the Semester in question and if not found
        # create one.
        # This scenario should be unlikely to happen as the "list" method in this
        # view set does provide a semester id for the current semester, which is
        # really what this code is about.
        #print("Request data dict")
        #print(json.dumps(request.data, indent=2))
        #print("End")
        if 'semester__year' in request.data and 'semester__sem' in request.data:
            req_data_dict = request.data.dict()
            #print("Request data dict")
            #print(json.dumps(req_data_dict))
            #print("End")

            # In order to change the request it has to
            # be made mutable.
            request.data._mutable = True
            year = int(req_data_dict['semester__year'])
            sem = req_data_dict['semester__sem']
            # remove semester__year and semester_sem from request
            # because request will be passed later on to
            # the create method and these keys are not known to it.
            request.data.pop('semester__year')
            request.data.pop('semester__sem')
            try:
                semester = Semester.objects.get(year=year,
                                                sem=sem)
            except ObjectDoesNotExist:
                # create semester
                semester = Semester.objects.create(year=year,
                                                   sem=sem)

            # add semester_id to the request
            request.data['semester_id'] = semester.id
            # make the request not editable now
            request.data._mutable = False

        resp = super().create(request, **kwargs)
        #print(json.dumps(resp.data, indent=2))
        return resp

    def list(self, request, **kwargs):
        #print("in CfPViewSet list method")
        resp = super().list(request, **kwargs)
        #print(json.dumps(resp.data, indent=2))

        return resp

    def update(self, request, **kwargs):
        #print("in CfPViewSet update method")
        #print(json.dumps(request.data, indent=2))
        resp = super().update(request, **kwargs)
        # print(json.dumps(resp.data, indent=2))
        return resp

    def get_queryset(self):
        # If you look at the model, you'll see we have user as a foreign key
        # and a related name "CfP_entry. This means we can get via the user the
        # objects that belong to this user.
        # So in the queries below, if we query this via a user, we should not
        # need the pi=self.request.GET.get('pi').
        # In reality, since we have the permissions.IsAuthenticated on, it means
        # we always have a user.
        # print("##****#### in queryset!!!!!")
        # cfp_id = self.request.GET.get('cfp_id', None)
        # Passing the request query dictionary directly to the filter db query.
        # https://stackoverflow.com/questions/11583870/django-is-it-possible-to-filter-on-querydict
        # https://coderwall.com/p/gtwm1q/pass-a-querydict-to-a-django-queryset
        return self.request.user.CfP_entry.select_related().filter(**self.request.GET.dict())
#        if cfp_id is not None:
#            #print("In get_queryset cfp_id not None")
#            return self.request.user.CfP_entry.select_related().filter(id=cfp_id)
#        elif self.request.GET.get('pi', None) is not None\
#                and self.request.GET.get('semester', None) is not None:
#            #print("In get_queryset pi and semester not None")
#            return self.request.user.CfP_entry.select_related().filter(pi=self.request.GET.get('pi'),
#                                                      semester=self.request.GET.get('semester'))
#        elif self.request.GET.get('semester', None) is not None:
#            #print("In get_queryset semester not None")
#            return self.request.user.CfP_entry.select_related().filter(semester=self.request.GET.get('semester'))
#        elif self.request.GET.get('pi', None) is not None:
#            print("In get_queryset pi not None")
#            # This was my default way of getting results for a given pi
#            return self.request.user.CfP_entry.filter(pi=self.request.GET.get('pi'))
#
#            from CfP_app.models import CfP, Semester
#            # study:
#            # https://docs.djangoproject.com/en/3.1/ref/models/relations/
#            # https://docs.djangoproject.com/en/3.1/ref/models/querysets/
#
#            # Reverse lookup.
#            # Start from semester and then look at what cfp objects have that semester.
#            #s = Semester.objects.get(id=6)
#            #cfp_obj = s.cfp_set.filter(pi=self.request.GET.get('pi'))
#
#            # To search for a
#            #print(myobj.semester)
#            #return cfp_obj
#        else:
#            #print("In get_queryset nothing pass, getting everything")
#            return self.request.user.CfP_entry.all()

#    def perform_create(self, serializer):
#        serializer.save(owner=self.request.user)
