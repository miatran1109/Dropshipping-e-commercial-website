from .models import Account, Order
from rest_framework import serializers



class AccountRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=500, min_length=5, write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'username', 'password', 'salt']



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['first_name','last_name','address','city','district','phone','email','note']