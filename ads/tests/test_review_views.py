import pytest
from django.urls import reverse
from rest_framework import status

from ads.models import Review


# Тест для анонимного пользователя
@pytest.mark.django_db
def test_review_anonymous_user_permissions(api_client, ad, review):
    """
    Тест на доступ анонимного пользователя к списку отзывов,
    а также проверка ошибок на другие операции.
    """
    list_url = reverse('ads:review-list', args=[ad.id])
    response = api_client.get(list_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    create_url = reverse('ads:review-create', args=[ad.id])
    response_create = api_client.post(create_url, data={})
    assert response_create.status_code == status.HTTP_401_UNAUTHORIZED

    detail_url = reverse('ads:review-detail', args=[review.id])
    response_detail = api_client.get(detail_url)
    assert response_detail.status_code == status.HTTP_401_UNAUTHORIZED

    update_url = reverse('ads:review-update', args=[review.id])
    response_update = api_client.patch(update_url, data={})
    assert response_update.status_code == status.HTTP_401_UNAUTHORIZED

    delete_url = reverse('ads:review-delete', args=[review.id])
    response_delete = api_client.delete(delete_url)
    assert response_delete.status_code == status.HTTP_401_UNAUTHORIZED


# Тест для другого пользователя
@pytest.mark.django_db
def test_ad_other_user_permissions(auth_user_2, ad, review):
    """
    Тест на доступ другого пользователя к списку отзывов,
    а также проверка ошибок на другие операции.
    """

    list_url = reverse('ads:review-list', args=[ad.id])
    response = auth_user_2.get(list_url)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert len(response_data['results']) == 1

    detail_url = reverse('ads:review-detail', args=[review.id])
    response_detail = auth_user_2.get(detail_url)
    assert response_detail.status_code == status.HTTP_200_OK

    update_url = reverse('ads:review-update', args=[review.id])
    response_update = auth_user_2.patch(update_url, data={})
    assert response_update.status_code == status.HTTP_403_FORBIDDEN

    delete_url = reverse('ads:review-delete', args=[review.id])
    response_delete = auth_user_2.delete(delete_url)
    assert response_delete.status_code == status.HTTP_403_FORBIDDEN


# Тесты для авторизованного пользователя

@pytest.mark.django_db
def test_review_create(auth_user, ad, user):
    """Тест для создания отзыва о товаре авторизованным пользователем."""
    url = reverse('ads:review-create', args=[ad.id])
    data = {'text': 'Отличный товар!'}

    response = auth_user.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED

    review = Review.objects.first()
    assert review.text == data['text']
    assert review.author == user
    assert review.ad == ad


@pytest.mark.django_db
def test_review_list_pagination(auth_user, ad, review, user):
    """Тест на проверку пагинации в списке отзывов."""
    Review.objects.create(
        text='Отзыв 2',
        author=user,
        ad=ad
    )

    url = reverse('ads:review-list', args=[ad.id])
    response = auth_user.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    ad.refresh_from_db()
    assert 'next' in response_data  # Проверка наличия пагинации
    assert len(response_data['results']) == 2


@pytest.mark.django_db
def test_reviews_list_authenticated_user(auth_user, ad, review):
    """Тест на просмотр списка отзывов авторизованным пользователем."""
    url = reverse('ads:review-list', args=[ad.id])
    response = auth_user.get(url)
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert len(response_data['results']) == 1
    assert response_data['results'][0]['text'] == review.text


@pytest.mark.django_db
def test_review_retrieve_owner(auth_user, ad, review):
    """Тест на просмотр отзыва владельцем."""
    url = reverse('ads:review-detail', args=[review.id])
    response = auth_user.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data['text'] == review.text
    assert response_data['author'] == ad.author.id


@pytest.mark.django_db
def test_reviews_update_owner_user(auth_user, review):
    """Тест на обновление отзыва владельцем."""
    url = reverse('ads:review-update', args=[review.id])
    new_data = {
        'text': 'Новый отзыв о товаре.'
    }

    response = auth_user.patch(url, new_data)
    response_2 = auth_user.patch(url, data={'text': ''})

    assert response.status_code == status.HTTP_200_OK
    assert response_2.status_code == status.HTTP_400_BAD_REQUEST

    # Проверяем, что данные обновились
    review.refresh_from_db()
    assert review.text == new_data['text']
    assert review.updated_at is not None
    assert review.text != ''


@pytest.mark.django_db
def test_review_destroy_by_author(auth_user, review):
    """Тест на удаление отзыва автором."""
    url = reverse('ads:review-delete', args=[review.id])
    response = auth_user.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Review.objects.filter(id=review.id).exists()


# Тесты для администратора
@pytest.mark.django_db
def test_review_create_admin(auth_admin, ad, admin):
    """Тест для создания отзыва о товаре администратором."""
    url = reverse('ads:review-create', args=[ad.id])
    data = {'text': 'Отличный товар!'}

    response = auth_admin.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED

    review = Review.objects.first()
    assert review.text == data['text']
    assert review.author == admin
    assert review.ad == ad


@pytest.mark.django_db
def test_reviews_list_admin_user(auth_admin, ad, review):
    """Тест на просмотр списка отзывов администратором."""
    url = reverse('ads:review-list', args=[ad.id])
    response = auth_admin.get(url)
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert len(response_data['results']) == 1
    assert response_data['results'][0]['text'] == review.text


@pytest.mark.django_db
def test_review_retrieve_admin(auth_admin, ad, review):
    """Тест на просмотр отзыва администратором."""
    url = reverse('ads:review-detail', args=[review.id])
    response = auth_admin.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert response_data['text'] == review.text
    assert response_data['author'] == ad.author.id


@pytest.mark.django_db
def test_reviews_update_admin(auth_admin, review):
    """Тест на обновление чужого отзыва администратором."""
    url = reverse('ads:review-update', args=[review.id])
    new_data = {
        'text': 'Новый отзыв о товаре.'
    }

    response = auth_admin.patch(url, new_data)
    response_2 = auth_admin.patch(url, data={'text': ''})

    assert response.status_code == status.HTTP_200_OK
    assert response_2.status_code == status.HTTP_400_BAD_REQUEST

    # Проверяем, что данные обновились
    review.refresh_from_db()
    assert review.text == new_data['text']
    assert review.updated_at is not None
    assert review.text != ''


@pytest.mark.django_db
def test_review_destroy_by_admin(auth_admin, review):
    """Тест на удаление чужого отзыва администратором."""
    url = reverse('ads:review-delete', args=[review.id])
    response = auth_admin.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Review.objects.filter(id=review.id).exists()
