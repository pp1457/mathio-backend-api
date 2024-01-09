from django.contrib.auth.models import User
from .models import UserProfile, UserContest
from rest_framework import serializers


class UserContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserContest
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    participated_contests = UserContestSerializer(many=True)
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()  # Serializer for UserProfile

    class Meta:
        model = User
        fields = '__all__'

class UserRegisterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('rating', )
        read_only_fields = fields
        

class UserRegisterSerializer(serializers.ModelSerializer):
    profile = UserRegisterProfileSerializer(write_only=True, required=False, label='')
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'profile')

    def validate(self, data):
        # Ensure password and password_confirm match
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def save(self, **kwargs):
        password_confirm = self.validated_data.pop('password_confirm', None)
        profile_data = self.validated_data.pop('profile', None)

        user = User.objects.create_user(**self.validated_data)

        # Check if UserProfile already exists for the user
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        # Update existing UserProfile if it already exists
        if profile_data and not created:
            for key, value in profile_data.items():
                setattr(user_profile, key, value)
            user_profile.save()

        return user

