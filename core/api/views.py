from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response

from rest_framework import (
    generics, mixins, pagination, permissions, status, viewsets
)
from api.serializers import (
    UserSerializer,
    CurrentUserSerializer,
    CurrentUsersPUTCHSerializer,
    PrivateListUsersSerializer,
    PrivateGETUsersSerializer,
)

from api.models import CitiesHintModel, MyUser
from api.permissions import IsOwnerOrReadOnly, IsAdmin


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 3
    page_query_param = 'page'
    page_size_query_param = 'size'
    ordering = 'date_joined'

    def get_paginated_response(self, data):
        query_size = self.request.query_params.get('size')

        if query_size is None:
            query_size = self.page_size

        return Response({
            'data': data,
            "meta": {
                'pagination': {
                    'total': self.page.paginator.num_pages,
                    'page': self.page.number,
                    'size': int(query_size)
                }
            },
        })


class UsersAPIView(generics.ListAPIView):
    """Paging data about users"""

    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberSetPagination


class CurrentUserView(generics.GenericAPIView):
    """Information available for user about yourself"""

    serializer_class = CurrentUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CurrentUserPUTCHView(mixins.UpdateModelMixin, generics.GenericAPIView):
    """Changing user data"""

    serializer_class = CurrentUsersPUTCHSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = MyUser.objects.all()

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        serializer_fields = list(serializer.fields.keys())
        for data_field in request.data.keys():
            if data_field not in serializer_fields:
                data = {
                    'code': 400,
                    'message': f'Changing {data_field} is not available'
                }
                return Response(data, status.HTTP_400_BAD_REQUEST)
        return self.partial_update(request, *args, **kwargs)


class PrivateUsersViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """Users CRUD viewset"""

    queryset = MyUser.objects.all()
    serializer_class = PrivateGETUsersSerializer
    pagination_class = PageNumberSetPagination
    permission_classes = (permissions.IsAuthenticated, IsAdmin)

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PrivateListUsersSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PrivateGETUsersSerializer(page, many=True)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Changing information about user"""

        if 'password' in request.data.keys():
            data = {"code": 400, "message": "Changing password not available"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if 'city' in request.data.keys():
            city = request.data.get('city')
            if CitiesHintModel.objects.filter(city=city).exists() is False:
                CitiesHintModel.objects.create(city=city)

        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)


class LoginView(generics.GenericAPIView):
    serializer_class = CurrentUserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        print(f'Запрос на логин {data=}')
        username = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:

                login(request, user)
                serializer = self.get_serializer(user)

                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_404_NOT_FOUND)


class LogoutView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)
