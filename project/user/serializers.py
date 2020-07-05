from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _  # Whenever we output
#   a message to the screen by using this we can easily transform it to be in
#   another language
import json
from rest_framework import serializers

# by using the rest_framework serializer ModelSerializer we get the build in
# functionality to send and read objects to and from the database.
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        # the class/model this serializer is based on
        # see core.User in core/models.py
        model = get_user_model()
        # fields converted to and from json when we do our http request
        # fields we want to make available to the API
        fields = ('email', 'password', 'name', 'partner')
        # allows to configure extra settings in our model serializer
        # in this case we make it to ensure the password:
        #  .- has the correct length
        #  .- it is write only and can not be read
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # There are a couple of methods I want to override from rest_framework
    # create
    # and
    # update
    def create(self, validated_data):
        """Create a new user with encrypted password and return the user"""
        # I already have this done in core.models.
        # See that get_user_model will get me core.User and the create_user
        # in UserManager will do the rest.
        print("User Serializer create")
        return get_user_model().objects.create_user(**validated_data)

    # the instance is going to be the model linked to our model serializer in
    # this case the user object.
    # The validated_data is going to be the fields in the "fields" above, that
    # should be validated.
    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        # I pop the password first from the data and we save/update that
        # as I don't want to save the password unencrypted.
        # After that if there is a password we set it and save the user.
        # Now the password is encrypted, set_password will do that.
        print("User Serializer update")
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()  # make sure it is character field
    password = serializers.CharField(  # no trimming and type is password
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        # in the validation we need to return the attributes back with the
        # user in it
        attrs['user'] = user
        return attrs
