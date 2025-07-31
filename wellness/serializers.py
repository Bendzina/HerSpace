from rest_framework import serializers
from .models import WisdomMessage, UserWisdomDelivery

class WisdomMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WisdomMessage
        fields = '__all__'

class UserWisdomDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWisdomDelivery
        fields = '__all__' 