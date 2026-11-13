import pytest
from wagtail.models import APIToken


@pytest.fixture
def api_token(django_user_model):
    user = django_user_model.objects.create_user(username="test")
    _obj, plaintext = APIToken.create_token(user=user, name="test")
    return plaintext
