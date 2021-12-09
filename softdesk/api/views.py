from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.serializers import UserSerializer, ProjectListSerializer, ProjectDetailSerializer
from api.mixins import GetDetailSerializerClassMixin
from api.models import Project


class SignupViewset(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectViewset(GetDetailSerializerClassMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        return Project.objects.filter(author_user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author_user_id"] = request.user.pk
        request.POST._mutable = False
        return super(ProjectViewset, self).create(request, *args, **kwargs)
