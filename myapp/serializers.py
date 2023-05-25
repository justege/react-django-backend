from rest_framework import serializers
from django.contrib.auth.models import User
from myapp.models import *

class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']  # Customize the fields as per your requirements

class ClientSerializer(serializers.ModelSerializer):
    id = UserSerializer()  # Serialize the related User object

    class Meta:
        model = Client
        fields = ['id', 'subscription', 'website', 'clientId']

class PopupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Popup
        fields = '__all__'


class PopupEngagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopupEngagement
        fields = '__all__'



class ChatGPTSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGPT
        fields = '__all__'
