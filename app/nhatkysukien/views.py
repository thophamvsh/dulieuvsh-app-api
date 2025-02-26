"""
Views for the nhật ký sự kiện APIs
"""
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Nhatkysukien, Xulysukientb
from nhatkysukien import serializers


class NhatkysukienViewSet(viewsets.ModelViewSet):
    """View for manage nhật ký sự kiện APIs."""
    serializer_class = serializers.NhatkysukienDetailSerializer
    queryset = Nhatkysukien.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve nhật ký sự kiện for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.NhatkysukienSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Tạo mới 1 nhật ký sự kiện"""
        serializer.save(user=self.request.user)


class XulysukientbViewset(mixins.DestroyModelMixin, mixins.UpdateModelMixin,
                          mixins.ListModelMixin, viewsets.GenericViewSet):
    """Quản lý xủ lý sự kiện TB trong cơ sở dữ liệu"""
    serializer_class = serializers.XulysukientbSerializer
    queryset = Xulysukientb.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-Tomay')
