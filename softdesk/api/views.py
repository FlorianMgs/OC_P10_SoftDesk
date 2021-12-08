from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import SignupUserSerializer


class SignupViewset(APIView):

    def post(self, request):
        serializer = SignupUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

