from rest_framework import serializers
from . import models


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'organization', 'bio', 'avatar', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
            'email': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        user = models.UserProfile.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            organization = validated_data['organization'],
            bio = validated_data['bio'],
            password = validated_data['password'],
            avatar = validated_data['avatar']
        )
        return user


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfileData
        fields = ('id', 'user_profile', 'title', 'image', 'video', 'posted_on',)
        extra_kwargs = {'user_profile': {'read_only': True}}


class FeaturedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FeaturedData
        fields = ('featured', )

        extra_kwargs = {"featured": {"read_only": True}}
        depth = 1