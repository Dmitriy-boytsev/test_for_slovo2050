from django.contrib.auth.models import User

from rest_framework import generics, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from tasks.models import ToDo
from tasks.serializers import RegisterSerializer, ToDoSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": {
                "username": user.username,
                "email": user.email
            }
        }, status=status.HTTP_201_CREATED)


class ToDoViewSet(viewsets.ModelViewSet):
    serializer_class = ToDoSerializer
    queryset = ToDo.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = ToDo.objects.filter(user=user)
        status = self.request.query_params.get('status')
        if status is not None:
            queryset = queryset.filter(completed=status.lower() == 'true')
        ordering = self.request.query_params.get('ordering')
        if ordering == 'date':
            queryset = queryset.order_by('created_at')
        elif ordering == 'status':
            queryset = queryset.order_by('completed')
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = ToDo.objects.get(pk=kwargs['pk'])
        except ToDo.DoesNotExist:
            return Response({'detail': 'Задача не найдена'}, status=status.HTTP_404_NOT_FOUND)
        if instance.user != request.user:
            return Response({'detail': 'Извини, мужик, ты не можешь посмотреть чужие записи'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
