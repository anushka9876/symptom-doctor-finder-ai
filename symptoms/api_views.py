from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SymptomInputSerializer, SymptomCheckSerializer
from .models import SymptomCheck, Disease
from .ml.spacy_extractor import extract_symptoms
from .ml.predictor import predict_disease
from .ml.emergency import check_emergency
from doctors.overpass import fetch_nearby_hospitals

class SymptomCheckAPIView(APIView):
    def post(self, request):
        ser = SymptomInputSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        text = ser.validated_data['symptoms_text']
        lat  = ser.validated_data['lat']
        lng  = ser.validated_data['lng']
        symptoms_found              = extract_symptoms(text)
        top3                        = predict_disease(symptoms_found)
        is_emergency, emergency_msg = check_emergency(symptoms_found)
        disease_obj, _ = Disease.objects.get_or_create(name=top3[0]['disease'])
        SymptomCheck.objects.create(
            user=request.user, raw_text=text,
            predicted_disease=disease_obj,
            confidence_score=top3[0]['confidence'],
            is_emergency=is_emergency,
        )
        hospitals = fetch_nearby_hospitals(lat, lng, top3[0]['disease'])
        return Response({
            'symptoms_found':   symptoms_found,
            'predictions':      top3,
            'is_emergency':     is_emergency,
            'emergency_msg':    emergency_msg,
            'nearby_hospitals': hospitals[:10],
        })

class SymptomHistoryAPIView(APIView):
    def get(self, request):
        checks = SymptomCheck.objects.filter(
            user=request.user).order_by('-created_at')[:20]
        return Response(SymptomCheckSerializer(checks, many=True).data)