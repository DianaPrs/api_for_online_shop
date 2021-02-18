import pytest
import random
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_405_METHOD_NOT_ALLOWED 
from rest_framework.authtoken.models import Token
from online_shop.models import Product, Order, Review, ProductCollection

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
def test_create_product(api_client, admin_user):
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
def test_get_product(api_client, product_factory):
    """Проверка получения списка товаров"""
    product = product_factory(_quantity=num)
    url = reverse('products-list')
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert len(resp_json) == num

@pytest.mark.django_db
def test_create_product_false(api_client,  user_factory):
    """Тест неуспешного создания товара"""
    url = reverse('products-list')
    data = {"name": "Test", "description": "test", "price": "15"}
    resp = api_client.post(url, data)
    assert resp.status_code == HTTP_401_UNAUTHORIZED
    user = user_factory()
    api_client.force_authenticate(user=user)
    resp = api_client.post(url, data)
    assert resp.status_code == HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_update_delete_product_false(api_client, admin_user,  user_factory):
    """Тест неуспешного обновления и удаления товара"""
    url = reverse('products-list')
    api_client.force_authenticate(user=admin_user)
    data = {"name": "Test", "description": "test", "price": "15"}
    resp = api_client.post(url, data)
    assert resp.status_code == HTTP_201_CREATED
    api_client.force_authenticate(user=None)
    product = Product.objects.get(name="Test")
    assert product.id
    assert product.name == "Test"
    url = reverse('products-detail', args=(product.id, ))
    resp = api_client.patch(url, {"price": "5"})
    assert resp.status_code == HTTP_401_UNAUTHORIZED
    user = user_factory()
    api_client.force_authenticate(user=user)
    resp = api_client.patch(url, {"price": "5"})
    assert resp.status_code == HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_update_delete_product(api_client, admin_user):
    """Тест успешного обновления и удаления товара"""
    url = reverse('products-list')
    api_client.force_authenticate(user=admin_user)
    data = {"name": "Test", "description": "test", "price": "15"}
    resp = api_client.post(url, data)
    assert resp.status_code == HTTP_201_CREATED
    product = Product.objects.get(name="Test")
    assert product.id
    assert product.name == "Test"
    url = reverse('products-detail', args=(product.id, ))
    resp = api_client.patch(url, {"price": "5"})
    assert resp.status_code == HTTP_200_OK
    update = Product.objects.get(name="Test")
    assert update.id == product.id
    assert update.price == 5
    resp = api_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT
    if Product.objects.filter(id=product.id).exists():
        assert False
  
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
def test_create_review_authorized_request(api_client, user_factory, product_factory):
   """Тест успешного создания отзыва авторизованным пользователем"""
   url = reverse('product-reviews-list')
   user = user_factory()
   product = product_factory()
   data = {"creator": user.id, "product_id": product.id, "text": "text"}
   api_client.force_authenticate(user=user)
   response = api_client.post(url, data)
   assert response.status_code == 201

@pytest.mark.django_db
def test_create_review_unauthorized_request(api_client, review_factory):
   """Тест неуспешного создания отзыва"""
   url = reverse('product-reviews-list')
   review = review_factory()
   data = {"creator": review.creator, "product_id": review.product_id, "text": review.text}
   response = api_client.post(url, data)
   assert response.status_code == HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_review_update_delete_false(api_client, user_factory, product_factory, review_factory):
    """Тест успешного обновления и удаления отзыва"""
    user = user_factory()   
    product = product_factory()
    review = review_factory(creator=user, product_id=product.id)
    url = reverse('product-reviews-detail', args=(review.id, ))
    api_client.force_authenticate(user=user)
    resp = api_client.patch(url, {"text": "Other text"})
    assert resp.status_code == HTTP_200_OK
    update = Review.objects.get(text="Other text")
    assert update.id == review.id
    assert update.text == "Other text"
    resp = api_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT
    if Review.objects.filter(id=review.id).exists():
        assert False

@pytest.mark.django_db
def test_get_review(api_client, review_factory):
    """Проверка получения 1го отзыва"""
    review = review_factory()
    url = reverse('product-reviews-detail', args=(review.id, ))
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert resp_json['id'] == review.id

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
def test_update_order_status_false(api_client, user_factory, order_factory):
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

@pytest.mark.django_db
def test_get_productcollection(api_client, productcollection_factory):
    """Проверка получения 1ой подборки."""
    productcollection = productcollection_factory()
    url = reverse('product-collections-detail', args=(productcollection.id, ))
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert resp_json['id'] == productcollection.id

@pytest.mark.django_db
def test_get_productcollection_list(api_client, productcollection_factory):
    """Проверка получения списка подборок."""
    productcollection = productcollection_factory(_quantity=num)
    url = reverse('product-collections-list')
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert len(resp_json) == num

@pytest.mark.django_db
def test_create_productcollection(api_client, admin_user, product_factory):
    """Проверка создания подборки."""
    url = reverse('product-collections-list')
    product = product_factory()
    api_client.force_authenticate(user=admin_user)
    data = {"headline": "test", "text": "test text", "items": product.id}
    resp = api_client.post(url, data)
    assert resp.status_code == HTTP_201_CREATED
    productcollection = ProductCollection.objects.get(headline="test")
    assert productcollection.id
    assert productcollection.headline == "test"

@pytest.mark.django_db
def test_update_delete_productcollection(api_client, productcollection_factory, admin_user):
    """Проверка обновления, удаления подборки"""
    productcollection = productcollection_factory()
    url = reverse('product-collections-detail', args=(productcollection.id, ))
    api_client.force_authenticate(user=admin_user)
    resp = api_client.patch(url, {"text": "other text"})
    assert resp.status_code == HTTP_200_OK
    update = ProductCollection.objects.get(text="other text")
    assert update.id == productcollection.id
    assert update.text == "other text"
    resp = api_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT
    if ProductCollection.objects.filter(id=productcollection.id).exists():
        assert False

@pytest.mark.django_db
def test_create_productcollection_false(api_client, user_factory, product_factory):
    """Проверка неуспешного создания подборки."""
    url = reverse('product-collections-list')
    product = product_factory()
    data = {"headline": "test", "text": "test text", "items": product.id}
    resp = api_client.post(url, data)
    assert resp.status_code == HTTP_401_UNAUTHORIZED
    user = user_factory()
    api_client.force_authenticate(user=user)
    resp = api_client.post(url, data)
    assert resp.status_code == HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_update_delete_productcollection_false(api_client, admin_user, product_factory, user_factory):
    """Проверка неуспешного обновления, удаления подборки."""
    url = reverse('product-collections-list')
    product = product_factory()
    api_client.force_authenticate(user=admin_user)
    data = {"headline": "test", "text": "test text", "items": product.id}
    resp = api_client.post(url, data)
    assert resp.status_code == HTTP_201_CREATED
    productcollection = ProductCollection.objects.get(headline="test")
    assert productcollection.id
    api_client.force_authenticate(user=None)
    resp = api_client.patch(url, {"text": "other text"})
    assert resp.status_code == HTTP_405_METHOD_NOT_ALLOWED
    resp = api_client.delete(url)
    assert resp.status_code == HTTP_405_METHOD_NOT_ALLOWED
    user = user_factory()
    api_client.force_authenticate(user=user)
    resp = api_client.patch(url, {"text": "other text"})
    assert resp.status_code == HTTP_405_METHOD_NOT_ALLOWED
    resp = api_client.delete(url)
    assert resp.status_code == HTTP_405_METHOD_NOT_ALLOWED
    if ProductCollection.objects.filter(id=productcollection.id).exists():
        assert True