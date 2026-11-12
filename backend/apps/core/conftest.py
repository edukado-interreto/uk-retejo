from datetime import datetime

import pytest
from wagtail.models import APIToken


@pytest.fixture
def api_token(django_user_model):
    ts = datetime.now().timestamp()
    user = django_user_model.objects.create_user(username=f"test-{ts}")
    _obj, plaintext = APIToken.create_token(user=user, name=f"token-{ts}")
    return plaintext
