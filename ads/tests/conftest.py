import pytest
from rest_framework.test import APIClient

from ads.models import Ad, Review
from users.models import User


@pytest.fixture
def api_client():
    """Фикстура клиента."""
    return APIClient()


@pytest.fixture
def user():
    """Фикстура для создания тестового пользователя."""

    user = User.objects.create(
        email='testuser@example.com',
        password='test-password',
        first_name='Test',
        last_name='User',
        phone='+7-900-000-00-01',
        role='user'
    )
    return user


@pytest.fixture
def user_2():
    """Фикстура для создания второго тестового пользователя."""
    user_2 = User.objects.create(
        email='user2@example.com',
        password='password',
        first_name='Test 2',
        last_name='User-2',
        phone='+7-900-000-00-02',
        role='user'
    )
    return user_2


@pytest.fixture
def admin():
    """Фикстура для создания администратора."""
    admin = User.objects.create(
        email='admin@example.com',
        password='admin-password',
        first_name='Test',
        last_name='Admin',
        phone='+7-900-000-00-02',
        role='admin'
    )
    return admin


@pytest.fixture
def ad(user):
    """Фикстура для тестового объявления."""
    ad = Ad.objects.create(
        title='Название 1',
        price=10_000,
        description='Описание товара 1.',
        author=user
    )
    return ad


@pytest.fixture
def review(user, ad):
    """Фикстура для отзыва авторизованным пользователем."""
    review = Review.objects.create(
        text='Отзыв 1',
        author=user,
        ad=ad
    )
    return review


@pytest.fixture
def auth_user(api_client, user):
    """Фикстура авторизованного пользователя."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def auth_admin(api_client, admin):
    """Фикстура авторизованного администратора."""
    api_client.force_authenticate(user=admin)
    return api_client


@pytest.fixture
def auth_user_2(api_client, user_2):
    """Фикстура авторизованного пользователя."""
    api_client.force_authenticate(user=user_2)
    return api_client
