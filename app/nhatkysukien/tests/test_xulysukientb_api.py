"""
Tests for the tags API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Xulysukientb

from nhatkysukien.serializers import XulysukientbSerializer


TAGS_URL = reverse('nhatkysukien:xulysukientb-list')


def detail_url(xulysukientb_id):
    """Tạo và trả về url xử lý sự kiện chi tiết"""
    return reverse('nhatkysukien:xulysukientb-detail', args=[xulysukientb_id])


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicTagsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving xử lý sự kiện thiết bị."""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving a list of tags."""
        Xulysukientb.objects.create(user=self.user, Tomay='H1')
        Xulysukientb.objects.create(user=self.user, Tomay='H2')

        res = self.client.get(TAGS_URL)

        xulysukientb = Xulysukientb.objects.all().order_by('-Tomay')
        serializer = XulysukientbSerializer(xulysukientb, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test list of tags is limited to authenticated user."""
        user2 = create_user(email='user2@example.com')
        Xulysukientb.objects.create(user=user2, Tomay='H2')
        xulysukientb = Xulysukientb.objects.create(user=self.user, Tomay='H1')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['Tomay'], xulysukientb.Tomay)
        self.assertEqual(res.data[0]['id'], xulysukientb.id)

    def test_update_tag(self):
        """Test cập nhật cho xử lý sự kiên TB."""
        xulysukientb = Xulysukientb.objects.create(user=self.user, Tomay='H2')

        payload = {
            'Tomay': 'H1', 'Noidung_xuly':
            'Cắt máy cắt',
            'Quatrinh_kiemtra': 'Theo dõi'
            }
        url = detail_url(xulysukientb.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        xulysukientb.refresh_from_db()
        self.assertEqual(xulysukientb.Tomay, payload['Tomay'])

    def test_delete_tag(self):
        """Test Xóa một xử lý sự kiện thiết bị"""
        xulysukientb = Xulysukientb.objects.create(user=self.user, Tomay='H2')

        url = detail_url(xulysukientb.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        xulysukientbs = Xulysukientb.objects.filter(user=self.user)
        self.assertFalse(xulysukientbs.exists())
