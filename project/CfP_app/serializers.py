from django.contrib.auth import get_user_model
from rest_framework import serializers
from CfP_app.models import Semester, CfP
from user.serializers import UserSerializer
import json
from django.db import models

'''
# Lead Serializer
class LeadSerializer(serializers.ModelSerializer):
  class Meta:
    model = Lead
    fields = '__all__'
'''


class SemesterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Semester
        #depth = 1
        fields = '__all__'
        exclude = []

# CfP Serializer
class CfPSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer(many=False, read_only=True)
    #https://www.vhinandrich.com/blog/saving-foreign-key-id-django-rest-framework-serializer
    semester_id = serializers.IntegerField(write_only=True)
    pi = UserSerializer(many=False, read_only=True)
    pi_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = CfP
        fields = '__all__'
        #fields = ('id', 'open_cfp', 'close_cfp', 'open_cfp_tz', 'close_cfp_tz',
        #          'pi', 'semester', 'semester_id')
        # https://stackoverflow.com/questions/40541822/how-to-show-depth-of-a-single-field-in-django-rest-framework
        #depth = 1
        #read_only_fields = ('semester_id',)
        exclude = []

    def create(self, validated_data):
        #print("In CfPSerializer update method ....")
        #profile_data = validated_data.pop('profile')
        #print("validated type:", type(validated_data))
        #print(validated_data)

        if 'pi_id' in validated_data:
            pi_id = validated_data.pop('pi_id')
            pi = get_user_model().objects.get(id=pi_id)
            if pi:
                validated_data['pi'] = pi

        if 'semester_id' in validated_data:
            semester_id = validated_data.pop('semester_id')
            semester = Semester.objects.get(id=semester_id)
            if semester:
                validated_data['semester'] = semester

        #return CfP.objects.create(**validated_data)
        return super().create(validated_data)


    def update(self, instance, validated_data):
        #print("In CfPSerializer update method ....")
        #print("instance type:", type(instance))
        #print("validated type:", type(validated_data))
        #print(validated_data)
        #print("instance semester:", instance.semester)
        #print("New semester:", Semester.objects.get(id=validated_data.pop('semester_id')))
        #instance.model_method()  # call model method for instance level computation
        instance.semester = Semester.objects.get(id=validated_data.pop('semester_id'))

        # call super to now save modified instance along with the validated data
        return super().update(instance, validated_data)
