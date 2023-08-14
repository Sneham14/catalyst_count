from rest_framework import serializers
from .models import UserModel, CompanyDataModel

class UserRegistrationSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=120, write_only=True)

    class Meta:
        model = UserModel
        fields = ('email', 'username', 'password', 'full_name')

    def create(self, validated_data):
        full_name = validated_data.pop('full_name')
        user = UserModel(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class CompanyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDataModel
        fields = '__all__'


class RecordCountSerializer(serializers.Serializer):
    total_records = serializers.IntegerField()

