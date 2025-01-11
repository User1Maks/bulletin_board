from decimal import Decimal
from django.core import mail
import pytest
from django.urls import reverse
from rest_framework import status

from ads.models import Ad


# Тест для анонимного пользователя
@pytest.mark.django_db
def test_ad_anonymous_user_permissions(api_client, ad):
    """
    Тест на доступ анонимного пользователя к списку объявлений,
    а также проверка ошибок на другие операции.
    """

    list_url = reverse('ads:ad-list')
    response = api_client.get(list_url)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert len(response_data['results']) == 1

    create_url = reverse('ads:ad-create')
    response_create = api_client.post(create_url, data={})
    assert response_create.status_code == status.HTTP_401_UNAUTHORIZED

    detail_url = reverse('ads:ad-detail', args=[ad.id])
    response_detail = api_client.get(detail_url)
    assert response_detail.status_code == status.HTTP_401_UNAUTHORIZED

    update_url = reverse('ads:ad-update', args=[ad.id])
    response_update = api_client.patch(update_url, data={})
    assert response_update.status_code == status.HTTP_401_UNAUTHORIZED

    delete_url = reverse('ads:ad-delete', args=[ad.id])
    response_delete = api_client.delete(delete_url)
    assert response_delete.status_code == status.HTTP_401_UNAUTHORIZED


# Тест для другого пользователя
@pytest.mark.django_db
def test_ad_other_user_permissions(auth_user_2, ad):
    """
    Тест на доступ другого пользователя к списку объявлений,
    а также проверка ошибок на другие операции.
    """

    list_url = reverse('ads:ad-list')
    response = auth_user_2.get(list_url)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert len(response_data['results']) == 1

    detail_url = reverse('ads:ad-detail', args=[ad.id])
    response_detail = auth_user_2.get(detail_url)
    assert response_detail.status_code == status.HTTP_200_OK

    update_url = reverse('ads:ad-update', args=[ad.id])
    response_update = auth_user_2.patch(update_url, data={})
    assert response_update.status_code == status.HTTP_403_FORBIDDEN

    delete_url = reverse('ads:ad-delete', args=[ad.id])
    response_delete = auth_user_2.delete(delete_url)
    assert response_delete.status_code == status.HTTP_403_FORBIDDEN


# Тесты для авторизованного пользователя

@pytest.mark.django_db
def test_ad_create(auth_user, user):
    """Тест на создание объявления авторизованным пользователем."""
    url = reverse("ads:ad-create")
    data = {
        'title': 'Тестовое название товара 1',
        'price': 10000.00,
        'description': 'Тестовое описание товара'
    }

    response = auth_user.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED

    assert response.data['title'] == data['title']
    assert Decimal(response.data['price']) == Decimal(data['price'])
    assert response.data['description'] == data['description']
    assert response.data['author'] == user.id

    assert Ad.objects.count() == 1
    ad = Ad.objects.first()
    assert ad.title == data['title']
    assert ad.price == data['price']
    assert ad.author == user


@pytest.mark.django_db
def test_ads_list_authenticated_user(auth_user, ad):
    """Тест на просмотр списка объявлений авторизованным пользователем."""
    url = reverse('ads:ad-list')
    response = auth_user.get(url)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert len(response_data['results']) == 1


@pytest.mark.django_db
def test_ad_list_pagination(api_client, ad, user):
    """Тест на проверку пагинации в списке объявлений."""
    Ad.objects.create(
        title='Название от пользователя 2',
        price=10_000,
        description='Описание товара пользователем 2.',
        author=user
    )

    url = reverse('ads:ad-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    ad.refresh_from_db()
    assert 'next' in response_data  # Проверка наличия пагинации
    assert len(response_data['results']) == 2


@pytest.mark.django_db
def test_user_specific_ads_list(auth_user, ad, user, ad_2):
    """Тест на просмотр списка объявлений, принадлежащих пользователю."""
    # Проверяем, что пользователь является автором объявления
    assert ad.author == user

    url = reverse('ads:my-list')
    response = auth_user.get(url)
    print(response.data)

    assert response.status_code == status.HTTP_200_OK

    assert len(response.data['results']) == 1
    assert response.data['results'][0]['title'] == ad.title
    # Проверка, что другие объявления пользователя другого авторов не появляются
    for item in response.data['results']:
        assert item['title'] != ad_2.title


@pytest.mark.django_db
def test_ad_retrieve_owner(auth_user, ad):
    """Тест на просмотр объявления владельцем."""
    url = reverse('ads:ad-detail', args=[ad.id])
    response = auth_user.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data['title'] == ad.title
    assert Decimal(response_data['price']) == Decimal(ad.price)
    assert response_data['description'] == ad.description
    assert response_data['author'] == ad.author.id


@pytest.mark.django_db
def test_ad_update_owner_user(auth_user, ad):
    """Тест на обновление объявления владельцем."""
    url = reverse('ads:ad-update', args=[ad.id])
    new_data = {
        'title': 'Новое название товара от владельца.',
        'price': 25000.00,
        'description': 'Новое описание товара от владельца.'
    }
    response = auth_user.patch(url, new_data)

    assert response.status_code == status.HTTP_200_OK

    # Проверяем, что данные обновились
    ad.refresh_from_db()
    assert ad.title == new_data['title']
    assert Decimal(ad.price) == Decimal(new_data['price'])
    assert ad.description == new_data['description']
    assert ad.updated_at is not None


@pytest.mark.django_db
def test_ad_destroy_by_author(auth_user, ad):
    """Тест на удаление объявления автором."""
    url = reverse('ads:ad-delete', args=[ad.id])
    response = auth_user.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Ad.objects.filter(id=ad.id).exists()
    assert Ad.objects.count() == 0


# Тесты для администратора

@pytest.mark.django_db
def test_ad_create_admin_user(auth_admin, admin):
    """Тест на создание объявления администратором."""
    url = reverse("ads:ad-create")
    data = {
        'title': 'Тестовое название от админа',
        'price': 10000.00,
        'description': 'Тестовое описание товара от админа'
    }

    response = auth_admin.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED

    assert response.data['title'] == data['title']
    assert Decimal(response.data['price']) == Decimal(data['price'])
    assert response.data['description'] == data['description']
    assert response.data['author'] == admin.id

    assert Ad.objects.count() == 1
    ad = Ad.objects.first()
    assert ad.title == data['title']
    assert ad.price == data['price']
    assert ad.author == admin


@pytest.mark.django_db
def test_ads_list_admin_user(auth_admin, ad):
    """Тест на просмотр списка объявлений администратором."""
    url = reverse("ads:ad-list")
    response = auth_admin.get(url)
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data['results']) == 1


@pytest.mark.django_db
def test_ad_retrieve_admin_user(auth_admin, ad):
    """Тест на просмотр объявления администратором."""
    url = reverse('ads:ad-detail', args=[ad.id])
    response = auth_admin.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data['title'] == ad.title
    assert Decimal(response_data['price']) == Decimal(ad.price)
    assert response_data['description'] == ad.description


@pytest.mark.django_db
def test_ad_update_admin_user(auth_admin, ad):
    """Тест на обновление объявления администратором."""
    url = reverse('ads:ad-update', args=[ad.id])
    new_data = {
        'title': 'Новое название товара от администратора',
        'price': 25000.00,
        'description': 'Новое описание товара от администратора'
    }
    response = auth_admin.patch(url, new_data)

    assert response.status_code == status.HTTP_200_OK

    # Проверяем, что данные обновились
    ad.refresh_from_db()
    assert ad.title == new_data['title']
    assert Decimal(ad.price) == Decimal(new_data['price'])
    assert ad.description == new_data['description']
    assert ad.updated_at is not None


@pytest.mark.django_db
def test_ad_destroy_by_admin(auth_admin, ad):
    """Тест на удаление объявления администратором."""
    url = reverse('ads:ad-delete', args=[ad.id])
    response = auth_admin.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Ad.objects.filter(id=ad.id).exists()
    assert Ad.objects.count() == 0


@pytest.mark.django_db
def send_email_test_setup(mailoutbox, auth_user, user):
    """Тест на отправку email для сброса пароля, а также на корректность
    данных отправленных в сообщении."""

    url = reverse('users:reset-password')
    data = {'email': user.email}
    response = auth_user.post(url, data)
    print(response.data)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    subject = 'Сброс пароля'
    body = ('Перейдите по ссылке для сброса пароля:'
            '{reset_link}. Если Вы не запрашивали сброс пароля '
            'проигнорируйте данное сообщение.')
    reset_link = 'http://127.0.0.1:8000/users/reset-password/{uid}/{token}/'
    body.format(reset_link.format(uid=user.uid, token='dummy_token'))

    mail.send_mail(
        subject=subject,
        message=body,
        from_email='testuser@example.com',
        recipient_list=[user.email]
    )

    assert len(mailoutbox) == 1  # Проверка, что письмо отправлено
    email = mailoutbox[0]
    assert email.subject == subject
    assert email.body == body
    # Проверка, что email пользователя в списке получателей
    assert user.email in email.to
