from rest_framework import serializers

class DoctorSerializer(serializers.Serializer):
    id          = serializers.CharField()
    name        = serializers.CharField()
    specialty   = serializers.CharField()
    fee         = serializers.CharField()
    latitude    = serializers.FloatField()
    longitude   = serializers.FloatField()
    distance_km = serializers.FloatField()
    address     = serializers.CharField()
    phone       = serializers.CharField()