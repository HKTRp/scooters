from rest_framework import serializers
from .models import *


class ScooterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Scooter
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = "__all__"


class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = "__all__"


class ScootersGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScootersGroup
        fields = "__all__"


class ClientsGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientsGroup
        fields = "__all__"


class RateGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = RateGroup
        fields = '__all__'


class GeoZoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeoPoint
        fields = '__all__'