import pytest
from rest_framework.test import APIClient

client = APIClient()

# @pytest.mark.django_db
def test_pytest_working():
    assert True == True
    response = client.post('posts/')
    assert response.status_code == 404
   
    