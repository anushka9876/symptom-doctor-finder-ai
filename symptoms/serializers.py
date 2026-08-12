from rest_framework import serializers
from .models import SymptomCheck

class SymptomInputSerializer(serializers.Serializer):
    symptoms_text = serializers.CharField()
    lat           = serializers.FloatField()
    lng           = serializers.FloatField()

class SymptomCheckSerializer(serializers.ModelSerializer):
    predicted_disease = serializers.StringRelatedField()
    class Meta:
        model  = SymptomCheck
        fields = ['id', 'raw_text', 'predicted_disease',
                  'confidence_score', 'is_emergency', 'created_at']