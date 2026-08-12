from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .overpass import fetch_nearby_hospitals
from .serializers import DoctorSerializer

class NearbyDoctorsAPIView(APIView):
    def get(self, request):
        try:
            lat     = float(request.query_params['lat'])
            lng     = float(request.query_params['lng'])
            disease = request.query_params.get('disease', '')
        except (KeyError, ValueError):
            return Response(
                {'error': 'lat and lng are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        hospitals  = fetch_nearby_hospitals(lat, lng, disease)
        serializer = DoctorSerializer(hospitals, many=True)
        return Response({
            'count':   len(hospitals),
            'disease': disease,
            'doctors': serializer.data,
        })