import pytest


@pytest.mark.django_db
def test_user_str(user):
    assert user.email == 'testuser@example.com'
    assert user.first_name == 'Test'
    assert user.last_name == 'User'
    assert user.phone == '+7-900-000-00-01'
    assert str(user) == f'{user.email}'


@pytest.mark.django_db
def test_ad_str(ad):
    assert ad.title == 'Название 1'
    assert ad.price == 10_000
    assert ad.description == 'Описание товара 1.'
    assert str(ad) == f'{ad.title} - {ad.price}'


@pytest.mark.django_db
def test_review_str(review, ad, user):
    assert review.text == 'Отзыв 1'
    assert review.author == user
    assert review.ad == ad

    assert str(review) == f'{review.text}'
