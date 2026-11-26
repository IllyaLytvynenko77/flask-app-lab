import io
import os
import sys
import pytest
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from products import db as product_db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    test_db = TinyDB(storage=MemoryStorage)
    product_db.products_table = test_db.table('products')

    with app.test_client() as client:
        yield client


def test_contact_form_validation_and_submission(client, tmp_path):
    # Некоректні дані (коротке ім'я, неправильний телефон)
    bad_resp = client.post('/contact', data={
        'name': 'Аня',
        'email': 'wrong-email',
        'phone': '0991234567',
        'subject': 'general',
        'message': 'Тест'
    }, follow_redirects=True)
    assert bad_resp.status_code == 200
    assert 'Довжина імені має бути від 4 до 10 символів'.encode('utf-8') in bad_resp.data

    # Коректні дані
    good_resp = client.post('/contact', data={
        'name': 'Олександр',
        'email': 'alex@example.com',
        'phone': '+380991234567',
        'subject': 'support',
        'message': 'Допоможіть налаштувати форму'
    }, follow_redirects=True)
    assert good_resp.status_code == 200
    assert 'Дані успішно відправлено та записано у лог-файл!'.encode('utf-8') in good_resp.data


def test_create_and_read_product(client):
    data = {
        'name': 'Ноутбук ASUS',
        'content': 'Потужний робочий ноутбук для програмування',
        'price': '32500.50',
        'category': 'electronics',
        'quantity': '4',
        'image': (io.BytesIO(b"fake png bytes"), 'laptop.png')
    }
    response = client.post('/product/add', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert response.status_code == 200
    assert 'Ноутбук ASUS'.encode('utf-8') in response.data

    # Перегляд одного товару
    detail_resp = client.get('/product/1')
    assert detail_resp.status_code == 200
    assert 'Потужний робочий ноутбук для програмування'.encode('utf-8') in detail_resp.data

    # Неіснуючий товар -> 404
    not_found_resp = client.get('/product/999')
    assert not_found_resp.status_code == 404


def test_update_product_preserves_id_and_created_at(client):
    client.post('/product/add', data={
        'name': 'Смартфон',
        'content': 'Базова модель',
        'price': '10000.00',
        'category': 'electronics',
        'quantity': '10'
    }, follow_redirects=True)

    original = product_db.products_table.get(product_db.ProductQuery.id == 1)
    orig_id = original['id']
    orig_created_at = original['created_at']

    response = client.post('/product/1/edit', data={
        'name': 'Смартфон Pro',
        'content': 'Оновлена версія з кращою камерою',
        'price': '14999.99',
        'category': 'electronics',
        'quantity': '7'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Смартфон Pro'.encode('utf-8') in response.data

    updated = product_db.products_table.get(product_db.ProductQuery.id == 1)
    assert updated['id'] == orig_id
    assert updated['created_at'] == orig_created_at
    assert updated['price'] == 14999.99


def test_delete_product(client):
    client.post('/product/add', data={
        'name': 'Книга Python',
        'content': 'Посібник з веб-розробки',
        'price': '650.00',
        'category': 'books',
        'quantity': '12'
    }, follow_redirects=True)

    response = client.post('/product/1/delete', follow_redirects=True)
    assert response.status_code == 200
    assert client.get('/product/1').status_code == 404
