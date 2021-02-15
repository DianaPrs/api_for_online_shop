import pytest
import random
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN 
from rest_framework.authtoken.models import Token
from online_shop.models import Product, Order

num = random.randint(2, 10)

@pytest.mark.django_db
def test_get_product(api_client, product_factory):
    """Проверка получения 1го товара"""
    product = product_factory()
    url = reverse('products-detail', args=(product.id, ))
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert resp_json['id'] == product.id

@pytest.mark.django_db
def test_product_create(api_client, admin_user):
    """Тест успешного создания товара"""
    url = reverse('products-list')
    api_client.force_authenticate(user=admin_user)
    data = {"name": "Test", "description": "test", "price": "15"}
    resp = api_client.post(url, data)
    assert resp.status_code == HTTP_201_CREATED
    product = Product.objects.get(name="Test")
    assert product.id
    assert product.name == "Test"

@pytest.mark.django_db
def test_create_user(api_client):
    """Тест регистрации пользователя"""
    data = {
    "email": "egg@mail.com",
    "username": "Egg",
    "password": "egg1988Y"
    }
    url = 'http://localhost:8000/api/v1/auth/users/'
    response = api_client.post(url, data)
    assert response.status_code == HTTP_201_CREATED
    user = User.objects.get(username="Egg")
    token = Token.objects.create(user=user)
    assert token.key

@pytest.mark.django_db
def test_authorized_request(api_client, user_factory, product_factory):
   """Тест успешного создания отзыва авторизованным пользователем"""
   url = reverse('product-reviews-list')
   user = user_factory()
   product = product_factory()
   data = {"creator": user.id, "product_id": product.id, "text": "text"}
   api_client.force_authenticate(user=user)
   response = api_client.post(url, data)
   assert response.status_code == 201

@pytest.mark.django_db
def test_unauthorized_request(api_client, review_factory):
   """Тест неуспешного создания отзыва"""
   url = reverse('product-reviews-list')
   review = review_factory()
   data = {"creator": review.creator, "product_id": review.product_id, "text": review.text}
   response = api_client.post(url, data)
   assert response.status_code == HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_get_review(api_client, review_factory):
    """Проверка получения 1го отзыва"""
    review = review_factory()
    url = reverse('product-reviews-detail', args=(review.id, ))
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK

@pytest.mark.django_db
def test_get_reviews_list(api_client, review_factory):
    """Проверка получения списка отзывов"""
    url = reverse('product-reviews-list')
    review = review_factory(_quantity=num)
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert len(resp_json) == num

@pytest.mark.django_db
def test_create_order(api_client, product_factory, user_factory):
   """Проверка создания заказа авторизованным пользователем"""
   url = reverse('orders-list')
   user = user_factory()
   product = product_factory()
   data = {"creator": user.id, "products": product.id}
   api_client.force_authenticate(user=user)
   response = api_client.post(url, data)
   assert response.status_code == HTTP_201_CREATED

@pytest.mark.django_db
def test_update_order_status(api_client, order_factory, admin_user):
    """Проверка обновления статуса заказа администратором"""
    order = order_factory()
    url = reverse('orders-detail', args=(order.id, ))
    api_client.force_authenticate(user=admin_user)
    resp = api_client.patch(url, {"status": "IN_PROGRESS"})
    assert resp.status_code == HTTP_200_OK
    update = Order.objects.get(id=order.id)
    assert update.id == order.id
    assert update.status == "IN_PROGRESS"

@pytest.mark.django_db
def test_update_order_status_dy_user(api_client, user_factory, order_factory):
    """Тест неуспешного обновления статуса заказа"""
    user = user_factory()
    order = order_factory(creator=user)
    url = reverse('orders-detail', args=(order.id, ))
    api_client.force_authenticate(user=user)
    resp = api_client.patch(url,  {"status": "DONE"})
    print(f'in order: {order.status}')
    print(f'in user: {user}')
    assert resp.status_code == 400
    api_client.force_authenticate(user=None)
    response = api_client.patch(url, {"status": "DONE"})
    assert response.status_code == HTTP_401_UNAUTHORIZED
