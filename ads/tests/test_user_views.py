import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_register(api_client):
    """Тест регистрации нового пользователя."""
    url = reverse('users:register')
    response = api_client.post(url, data={'email': 'user1@mail.ru',
                                          'password': 'Useruser1!'})
    assert response.status_code == 201
    response_data = response.json()
    assert response_data['email'] == 'user1@mail.ru'
    assert 'id' in response_data
