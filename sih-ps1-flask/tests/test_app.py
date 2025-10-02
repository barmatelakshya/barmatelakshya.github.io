from flask import Flask
import pytest

# Assuming the Flask app is defined in app.py
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'SIH PS1 Project' in response.data
    assert b'New Smart India Hackathon Project Started' in response.data
    assert b'Project Initialized Successfully' in response.data

def test_api_status(client):
    response = client.get('/api/status')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['project'] == 'SIH PS1'
    assert json_data['status'] == 'initialized'
    assert json_data['message'] == 'New project ready for development'