"""
URL mappings for the nhật ký sự kiện app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from nhatkysukien import views


router = DefaultRouter()
router.register('themnhatkysukien', views.NhatkysukienViewSet)
router.register('xulysukientb', views.XulysukientbViewset)

app_name = 'nhatkysukien'

urlpatterns = [
    path('', include(router.urls)),
]
