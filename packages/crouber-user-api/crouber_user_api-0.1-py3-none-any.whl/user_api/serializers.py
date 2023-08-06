# from rest_framework import serializers
from user_api.models import CustomUser
from profile_api.serializers import ProfileSerializer
from djoser.serializers import UserSerializer
from djoser.compat import get_user_email, get_user_email_field_name
from django.contrib.auth import get_user_model
from djoser.conf import settings


User = get_user_model()


class CustomUserSerializer(UserSerializer):

    profile = ProfileSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = ['firstname', 'lastname', 'email', 'profile',
                  'modified_date', 'created_date', 'password']
        # extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['modified_date', 'created_date']

    # Implement the create() method as the default does not address
    # writeable nested serializer objects
    # def create(self, validated_data):

        # user = CustomUser.objects.create_user(**validated_data)  # noqa: used defined manager.py

        # return user

    def update(self, instance, validated_data):
        instance.firstname = validated_data.get(
            'firstname', instance.firstname)
        instance.lastname = validated_data.get(
            'lastname', instance.lastname)
        instance.save()
        # Handle Email upadate
        email_field = get_user_email_field_name(User)
        if settings.SEND_ACTIVATION_EMAIL and email_field in validated_data:
            instance_email = get_user_email(instance)
            if instance_email != validated_data[email_field]:
                instance.is_active = False
                instance.save(update_fields=["is_active"])
        # Handle profile update
        if 'profile' in validated_data:
            profile_data = validated_data.pop('profile')
            profile = instance.profile

            profile.middle_initial = profile_data.get(
                'middle_initial', profile.middle_initial)
            profile.profile_name = profile_data.get(
                'profile_name', profile.profile_name)
            profile.birth_date = profile_data.get(
                'birth_date', profile.birth_date)
            profile.phonenumber = profile_data.get(
                'phonenumber', profile.phonenumber)
            profile.profile_image = profile_data.get(
                'profile_image', profile.profile_image)
            profile.address1 = profile_data.get(
                'address1', profile.address1)
            profile.address2 = profile_data.get(
                'address2', profile.address2)
            profile.zip_code = profile_data.get(
                'zip_code', profile.zip_code)
            profile.city = profile_data.get(
                'city', profile.city)
            profile.state = profile_data.get(
                'state', profile.state)
            profile.country = profile_data.get(
                'country', profile.country)
            profile.save()

        return instance
