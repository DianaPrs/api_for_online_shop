import uuid
import pytest
from django.conf import settings
from rest_framework.test import APIClient
from model_bakery import baker

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def product_factory():

    def factory(**kwargs):
        return baker.make('Product', **kwargs)
    
    return factory


@pytest.fixture
def review_factory():

    def factory(**kwargs):
        return baker.make('Review', **kwargs)
    
    return factory

@pytest.fixture
def user_factory():

    def factory(**kwargs):
        return baker.make(settings.AUTH_USER_MODEL)

    return factory

@pytest.fixture
def order_factory():

    def factory(**kwargs):
        return baker.make('Order', **kwargs)
    
    return factory

@pytest.fixture
def productcollection_factory():

    def factory(**kwargs):
        return baker.make('ProductCollection', **kwargs)
    
    return factory