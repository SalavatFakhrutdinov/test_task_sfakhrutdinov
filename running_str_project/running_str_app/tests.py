from django.test import TestCase
import pytest
from django.urls import reverse
from .models import TextRequest


@pytest.mark.django_db
def test_index_view(client):
    # Проверка, что главная страница загружается
    response = client.get(reverse('index'))  # Убедитесь, что у вас есть соответствующее имя URL
    assert response.status_code == 200
    assert b'Input a string' in response.content  # Убедитесь, что текст формы присутствует


@pytest.mark.django_db
def test_text_request_creation(client):
    # Проверка создания TextRequest
    response = client.post(reverse('index'), data={
        'text': 'Test text',
        'duration': 5
    })
    assert response.status_code == 200

    # Проверка, что объект был создан в базе данных
    assert TextRequest.objects.count() == 1
    text_request = TextRequest.objects.first()
    assert text_request.text == 'Test text'
    assert text_request.duration == 5


@pytest.mark.django_db
def test_text_request_creation_invalid_duration(client):
    # Проверка обработки неправильного ввода для поля duration
    response = client.post(reverse('index'), data={
        'text': 'Test text',
        'duration': -1  # Неверное значение
    })
    # Также предполагаем, что в случае ошибки статус вернёт 400
    assert response.status_code in [200, 400]

    # Проверка, что объект не был создан в базе данных
    assert TextRequest.objects.count() == 0


@pytest.mark.django_db
def test_text_request_creation_invalid(client):
    # Проверка обработки неправильного ввода (например, пустое текстовое поле)
    response = client.post(reverse('index'), data={
        'text': '',
        'duration': 5
    })
    # Здесь мы предполагаем, что в случае ошибки форма вернёт статус 400 или 200,
    # в зависимости от представления
    assert response.status_code in [200, 400]

    # Проверка, что объект не был создан в базе данных
    assert TextRequest.objects.count() == 0
