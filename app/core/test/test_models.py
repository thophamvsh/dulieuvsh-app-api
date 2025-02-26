"""
Tests for models.
"""
from unittest.mock import patch
from decimal import Decimal
from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create a return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models."""
    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""

        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample receipe description.',
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """Test creating an ingredient is successful."""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Ingredient1'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/recipe/{uuid}.jpg')

    def test_create_nhatkysukien(self):
        """Test tạo nhật ký sự kiện trước, sau đó thêm xử lý sự kiện"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )

        # Bước 1: Tạo `Nhatkysukien` trước, chưa có `Xulysukientb`
        nhatkysukien = models.Nhatkysukien.objects.create(
            user=user,
            title='Mẫu nhật ký sự kiện',
            Thoigian=datetime.strptime('2025-05-24', '%Y-%m-%d').date(),
            Hethong_Thietbi='Hệ thống cơ khí',
            Hientuong_Dienbien='Tiếng ồn lớn khi vận hành',
        )
        # Tạo các biến riêng cho chuỗi thời gian và định dạng
        time_string = '2025-05-24 12:00:00'
        time_format = '%Y-%m-%d %H:%M:%S'
        Thoigian_xuly = datetime.strptime(time_string, time_format)

        # Bước 2: Đảm bảo `Xulysukientb` được tạo
        xulysukientb = models.Xulysukientb.objects.create(
            user=user,
            title='Mẫu xử lý sự kiện',
            Tomay='Hệ thống máy xử lý',
            Noidung_xuly='Xử lý lỗi phần cứng',
            Thoigian_xuly=Thoigian_xuly,
        )
        # Bước 3: Liên kết `Nhatkysukien` với `Xulysukientb`
        nhatkysukien.xulysukientbs.add(xulysukientb)
        # Kiểm tra xem đối tượng có được liên kết chính xác không
        self.assertEqual(nhatkysukien.xulysukientbs.count(), 1)
        self.assertIn(xulysukientb, nhatkysukien.xulysukientbs.all())
