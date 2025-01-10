import pytest
from django.urls import reverse
from rest_framework import status

from users.models import User


# Тесты для анонимного пользователя
@pytest.mark.django_db
def test_register(api_client):
    """Тест регистрации нового пользователя."""
    url = reverse('users:register')
    data = {
        'email': 'user1@mail.ru',
        'first_name': 'New',
        'last_name': 'User',
        'phone': '+79000000003',
        'password': 'Useruser1!'
    }
    data_2 = {
        'email': 'userailu',
        'password': '123'
    }

    response = api_client.post(url, data=data)
    response_2 = api_client.post(url, data=data_2)

    assert response.status_code == status.HTTP_201_CREATED
    assert response_2.status_code == status.HTTP_400_BAD_REQUEST

    response_data = response.json()
    assert response_data['email'] == 'user1@mail.ru'
    assert 'id' in response_data
    assert response_data['first_name'] == 'New'
    assert response_data['last_name'] == 'User'
    assert response_data['phone'] == '+79000000003'

    user = User.objects.get(email=data['email'])
    assert user.is_active is True


@pytest.mark.django_db
def test_user_anonymous_permissions(api_client, user):
    """Тесты на права доступа анонимного пользователя."""

    list_url = reverse('users:user-list')
    response = api_client.get(list_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    detail_url = reverse('users:profile')
    response_detail = api_client.get(detail_url)
    assert response_detail.status_code == status.HTTP_401_UNAUTHORIZED

    update_url = reverse('users:update-profile')
    response_update = api_client.patch(update_url, data={})
    assert response_update.status_code == status.HTTP_401_UNAUTHORIZED

    delete_url = reverse('users:user-delete', args=[user.pk])
    response_delete = api_client.delete(delete_url)
    assert response_delete.status_code == status.HTTP_401_UNAUTHORIZED


# Тесты для авторизованного пользователя
@pytest.mark.django_db
def test_user_list_authenticated(auth_user):
    """
    Тест для авторизованного пользователя, который получает список
    пользователей.
    """
    url = reverse('users:user-list')
    response = auth_user.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    # Проверка, что в ответе содержится хотя бы один пользователь
    assert len(response_data) > 0


@pytest.mark.django_db
def test_user_delete_authenticated(auth_user, user):
    """Тест для проверки удаления пользователя."""
    assert User.objects.filter(id=user.pk).exists()

    url = reverse('users:user-delete', args=[user.pk])
    response = auth_user.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Дополнительно, можно проверить, что пользователь был удален
    assert not User.objects.filter(id=user.pk).exists()
