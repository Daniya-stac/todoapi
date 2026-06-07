from main import app
from starlette.testclient import TestClient
import pytest

client = TestClient(app)


def test_all_todos():
    response = client.get('/todos/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_task():
    taste_data = {
        "description": "КХЕХЕХХЕЕХЕ",
        "date": "2026-06-04T13:36:48.413Z",
        "completed": False
    }
    response = client.post('/todos/', json=taste_data)
    assert response.status_code == 201
    data = response.json()
    assert data['description'] == taste_data['description']
    assert 'id' in data


def test_spec_task():
    taste_data = {
        "description": "КХЕХЕХХЕЕХЕ",
        "date": "2026-06-04T13:36:48.413Z",
        "completed": False
    }
    response1 = client.post('/todos/', json=taste_data)
    task_id = response1.json()['id']
    response2 = client.get(f'/todos/{task_id}/')
    assert response2.status_code == 200
    assert response2.json()['id'] == task_id


def test_delete():
    taste_data = {
        "description": "КХЕХЕХХЕЕХЕ",
        "date": "2026-06-04T13:36:48.413Z",
        "completed": False
    }
    response1 = client.post('/todos/', json=taste_data)
    task_id = response1.json()['id']
    response2 = client.delete(f'/todos/{task_id}/')
    assert response2.status_code == 204
    response3 = client.get(f'/todos/{task_id}/')
    assert response3.status_code == 404


def test_change():
    taste_data = {
        "description": "КХЕХЕХХЕЕХЕ",
        "date": "2026-06-04T13:36:48.413Z",
        "completed": False
    }

    ch_test = {"completed": True}

    response1 = client.post('/todos/', json=taste_data)
    task_id = response1.json()['id']
    response2 = client.patch(f'/todos/{task_id}/', json=ch_test)
    des_val = response2.json()['description']
    bool_val = response2.json()['completed']
    assert response2.status_code == 200
    assert bool_val == ch_test['completed']
    assert des_val == taste_data['description']
