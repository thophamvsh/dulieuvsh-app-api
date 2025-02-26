from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Nhatkysukien, Xulysukientb
from nhatkysukien.serializers import (
    NhatkysukienSerializer,
    NhatkysukienDetailSerializer,
    )


NHATKYSUKIEN_URL = reverse('nhatkysukien:nhatkysukien-list')


def detail_url(nhatkysukien_id):
    """Tạo và trả về nhật ký sự kiện chi tiết"""
    return reverse('nhatkysukien:nhatkysukien-detail', args=[nhatkysukien_id])


def create_nhatkysukien(user, **params):
    """Tạo và trả về mẫu của nhật ký sự kiện"""
    defaults = {
        'title': 'Sample recipe title',
        'Hethong_Thietbi': 'Hiện tượng diễn biến sự kiện',
        'Hientuong_Dienbien': 'Hiện tượng diễn biến sự kiện',
        'Quatrinh_Kt': 'Hiện tượng diễn biến sự kiện',
        'LoaiSc': 'Hiện tượng diễn biến sự kiện',
        'Baocao_Chidao': 'Hiện tượng diễn biến sự kiện',
        'DeNghi': 'Hiện tượng diễn biến sự kiện',
        'CaVanHanh': 'Hiện tượng diễn biến sự kiện',
        'Donvi_khacPhuc': 'Hiện tượng diễn biến sự kiện',
        }
    defaults.update(params)

    nhatkysukien = Nhatkysukien.objects.create(user=user, **defaults)
    return nhatkysukien


def create_user(**params):
    """Tạo và trả về một user mới"""
    return get_user_model().objects.create_user(**params)


class PublicNhatkysukienAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(NHATKYSUKIEN_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateNhatkysukienApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""
        create_nhatkysukien(user=self.user)
        create_nhatkysukien(user=self.user)
        res = self.client.get(NHATKYSUKIEN_URL)

        nhatkysukiens = Nhatkysukien.objects.all().order_by('-id')
        serializer = NhatkysukienSerializer(nhatkysukiens, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_nhatkysukien_list_limited_to_user(self):
        """Test list of recipes is limited to authenticated user."""
        other_user = create_user(email='other@example.com', password='test123')
        create_nhatkysukien(user=other_user)
        create_nhatkysukien(user=self.user)
        res = self.client.get(NHATKYSUKIEN_URL)

        nhatkysukiens = Nhatkysukien.objects.filter(user=self.user)
        serializer = NhatkysukienSerializer(nhatkysukiens, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_nhatkysukien_detail(self):

        """Kiểm tra nhật ký sự kiện chi tiết."""
        nhatkysukien = create_nhatkysukien(user=self.user)

        url = detail_url(nhatkysukien.id)
        res = self.client.get(url)

        serializer = NhatkysukienDetailSerializer(nhatkysukien)
        self.assertEqual(res.data, serializer.data)

    def test_create_nhatkysukien(self):
        """Kiểm tra tạo một Nhật ký sự kiện"""
        payload = {
            'title': 'Sample recipe title',
            'Hethong_Thietbi': 'Hiện tượng diễn biến sự kiện',
            'Hientuong_Dienbien': 'Hiện tượng diễn biến sự kiện',
            'Quatrinh_Kt': 'Hiện tượng diễn biến sự kiện',
            'LoaiSc': 'Hiện tượng diễn biến sự kiện',
            'Baocao_Chidao': 'Hiện tượng diễn biến sự kiện',
            'DeNghi': 'Hiện tượng diễn biến sự kiện',
            'CaVanHanh': 'Hiện tượng diễn biến sự kiện',
            'Donvi_khacPhuc': 'Hiện tượng diễn biến sự kiện',
        }
        res = self.client.post(NHATKYSUKIEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        nhatkysukien = Nhatkysukien.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(nhatkysukien, k), v)
        self.assertEqual(nhatkysukien.user, self.user)

    def test_partial_update(self):
        """Test partial update of a nhật ký sự kiện."""

        nhatkysukien = create_nhatkysukien(
            user=self.user,
            title='Sample recipe title',
            Hethong_Thietbi='Hiện tượng diễn biến sự kiện',
            Hientuong_Dienbien='Hiện tượng diễn biến sự kiện',
            Quatrinh_Kt='Hiện tượng diễn biến sự kiện',
            LoaiSc='Hiện tượng diễn biến sự kiện',
            Baocao_Chidao='Hiện tượng diễn biến sự kiện',
            DeNghi='Hiện tượng diễn biến sự kiện',
            CaVanHanh='Hiện tượng diễn biến sự kiện',
            Donvi_khacPhuc='Hiện tượng diễn biến sự kiện',
        )

        payload = {'title': 'New recipe title'}
        url = detail_url(nhatkysukien.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        nhatkysukien.refresh_from_db()
        self.assertEqual(nhatkysukien.title, payload['title'])
        self.assertEqual(nhatkysukien.user, self.user)

    def test_full_update(self):
        """Test full update of recipe."""
        nhatkysukien = create_nhatkysukien(
            user=self.user,
            title='Sample recipe title',
            Hethong_Thietbi='Hiện tượng diễn biến sự kiện',
            Hientuong_Dienbien='Hiện tượng diễn biến sự kiện',
            Quatrinh_Kt='Hiện tượng diễn biến sự kiện',
            LoaiSc='Hiện tượng diễn biến sự kiện',
            Baocao_Chidao='Hiện tượng diễn biến sự kiện',
            DeNghi='Hiện tượng diễn biến sự kiện',
            CaVanHanh='Hiện tượng diễn biến sự kiện',
            Donvi_khacPhuc='Hiện tượng diễn biến sự kiện',
        )

        payload = {
            'title': 'Sample recipe title',
            'Hethong_Thietbi': 'Hiện tượng diễn biến sự kiện',
            'Hientuong_Dienbien': 'Hiện tượng diễn biến sự kiện',
            'Quatrinh_Kt': 'Hiện tượng diễn biến sự kiện',
            'LoaiSc': 'Hiện tượng diễn biến sự kiện',
            'Baocao_Chidao': 'Hiện tượng diễn biến sự kiện',
            'DeNghi': 'Hiện tượng diễn biến sự kiện',
            'CaVanHanh': 'Hiện tượng diễn biến sự kiện',
            'Donvi_khacPhuc': 'Hiện tượng diễn biến sự kiện',
        }
        url = detail_url(nhatkysukien.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        nhatkysukien.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(nhatkysukien, k), v)
        self.assertEqual(nhatkysukien.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the recipe user results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        nhatkysukien = create_nhatkysukien(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(nhatkysukien.id)
        self.client.patch(url, payload)

        nhatkysukien.refresh_from_db()
        self.assertEqual(nhatkysukien.user, self.user)

    def test_delete_nhatkysukien(self):
        """Test deleting a nhật ký sự kiện successful."""
        nhatkysukien = create_nhatkysukien(user=self.user)

        url = detail_url(nhatkysukien.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Nhatkysukien.objects.filter(id=nhatkysukien.id).exists()
            )

    def test_recipe_other_users_nhatkysukien_error(self):
        """Test trying to delete another users nhật ký sự kiện gives error."""
        new_user = create_user(email='user2@example.com', password='test123')
        nhatkysukien = create_nhatkysukien(user=new_user)

        url = detail_url(nhatkysukien.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(
            Nhatkysukien.objects.filter(id=nhatkysukien.id).exists()
            )

    def test_create_nhatkysukien_with_new_xulysukientbs(self):
        """Kiểm tra tạo mới 1 nhật ký sự kiện với xử lý sựu kiện"""
        payload = {
            'title': 'nhật ký sự kiện',
            'Hethong_Thietbi': 'Hiện tượng diễn biến sự kiện',
            'Hientuong_Dienbien': 'Hiện tượng diễn biến sự kiện',
            'xulysukientbs': [{'Tomay': 'H1'}, {'Tomay': 'H2'}],
        }
        res = self.client.post(NHATKYSUKIEN_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        nhatkysukiens = Nhatkysukien.objects.filter(user=self.user)
        self.assertEqual(nhatkysukiens.count(), 1)
        nhatkysukien = nhatkysukiens[0]
        self.assertEqual(nhatkysukien.xulysukientbs.count(), 2)
        for xulysukientb in payload['xulysukientbs']:
            exists = nhatkysukien.xulysukientbs.filter(
                Tomay=xulysukientb['Tomay'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)

    def test_create_nhatkysukien_with_existing_xulysukientbs(self):
        """nhật ký sự kiện with existing Xulysukientb."""
        xulysukientb_indian = Xulysukientb.objects.create(
            user=self.user, Tomay='Indian'
         )
        payload = {
            'title': 'Nhật ký sự kiện',
            'Hethong_Thietbi': 'Hiện tượng diễn biến sự kiện',
            'Hientuong_Dienbien': 'Hiện tượng diễn biến sự kiện',
            'xulysukientbs': [
                {'Tomay': 'Indian'},
                {'Tomay': 'H2'}
                ],  # Đảm bảo 'Indian' đã có
        }

        res = self.client.post(NHATKYSUKIEN_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        nhatkysukiens = Nhatkysukien.objects.filter(user=self.user)
        self.assertEqual(nhatkysukiens.count(), 1)

        nhatkysukien = nhatkysukiens.first()
        self.assertEqual(nhatkysukien.xulysukientbs.count(), 2)

        # 🛠 In ra ID để kiểm tra
        print(f"Expected: {xulysukientb_indian.id}")
        for xulysukientb in nhatkysukien.xulysukientbs.all():
            print(f"Actual: {xulysukientb.id}")
        # Kiểm tra xem `xulysukientb_indian` có đúng ID không
        self.assertIn(xulysukientb_indian, nhatkysukien.xulysukientbs.all())

    def test_create_xulysukientb_on_update(self):
        """test tạo Xulysukientb khi update Nhatkysukien."""
        nhatkysukien = create_nhatkysukien(user=self.user)

        payload = {'xulysukientbs': [{'Tomay': 'H1'}]}
        url = detail_url(nhatkysukien.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_xulysukientb = Xulysukientb.objects.get(user=self.user, Tomay='H1')
        self.assertIn(new_xulysukientb, nhatkysukien.xulysukientbs.all())

    def test_update_nhatkysukien_assign_xulysukientb(self):
        """Kiểm tra tồn tại Xulysukientb when updating a Nhatkysukien."""
        xulysukientb_old = Xulysukientb.objects.create(
            user=self.user, Tomay='OldEvent'
            )
        nhatkysukien = create_nhatkysukien(user=self.user)
        nhatkysukien.xulysukientbs.add(xulysukientb_old)

        xulysukientb_new = Xulysukientb.objects.create(
            user=self.user, Tomay='NewEvent'
            )
        payload = {'xulysukientbs': [{'Tomay': 'NewEvent'}]}
        url = detail_url(nhatkysukien.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(
            xulysukientb_new,
            nhatkysukien.xulysukientbs.all()
            )
        self.assertNotIn(
            xulysukientb_old,
            nhatkysukien.xulysukientbs.all()
            )

    def test_clear_nhatkysukien_xulysukientbs(self):
        """Test clearing a Nhatkysukien's Xulysukientbs."""
        xulysukientb = Xulysukientb.objects.create(
            user=self.user, Tomay='ClearEvent'
            )
        nhatkysukien = create_nhatkysukien(user=self.user)
        nhatkysukien.xulysukientbs.add(xulysukientb)

        payload = {'xulysukientbs': []}
        url = detail_url(nhatkysukien.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(nhatkysukien.xulysukientbs.count(), 0)
