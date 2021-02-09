from .models import Account
from rest_framework import serializers



class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=5, write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('Username should only contain alphanumeric character')
        return attrs

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)  # if not pass it here it will sent back only the username

class AccountLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 50, min_length = 5, write_only = True)

    class Meta:
        model = Account
        fields = ['email', 'password']