from api.models import CitiesHintModel, MyUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for all users"""

    class Meta:
        model = MyUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
        ]


class CurrentUserSerializer(serializers.ModelSerializer):
    """Serializer for user about yourself"""

    class Meta:
        model = MyUser
        fields = [
            'first_name',
            'last_name',
            'other_name',
            'email',
            'phone',
            'birthday',
            'is_admin',
        ]


class CurrentUsersPUTCHSerializer(serializers.ModelSerializer):
    """Serializer available data for edit"""

    class Meta:
        model = MyUser
        fields = [
            'first_name',
            'last_name',
            'other_name',
            'email',
            'phone',
            'birthday',
        ]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CitiesHintModel
        fields = ('city',)


class PrivateLISTUsersSerializer(serializers.ModelSerializer):
    """Serializer data about users for admin"""

    class Meta:
        model = MyUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'email'
        ]


class PrivateGETUsersSerializer(serializers.ModelSerializer):
    """Serializer data all users available for admin"""
    city = serializers.SlugRelatedField(
        slug_field="city", queryset=CitiesHintModel.objects.all(),
        required=False
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser

        fields = [
            'id',
            'first_name',
            'last_name',
            'other_name',
            'email',
            'phone',
            'birthday',
            'city',
            'additional_info',
            'is_admin',
            'password'
        ]
        optional_fields = ('city', 'password')

    def create(self, validated_data):
        instance = MyUser.objects.create_user(**validated_data)
        return instance
