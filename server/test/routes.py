# tests/test_app.py

import pytest
from app import app, db
from models import Hero, Power, HeroPower



def test_create_hero(client):
    response = client.post('/heroes', json={"name": "Test Hero", "super_name": "Test Superhero"})
    assert response.status_code == 201

def test_get_hero(client):
    test_hero = Hero(name="Test Hero", super_name="Test Superhero")
    db.session.add(test_hero)
    db.session.commit()
    response = client.get('/hero/1')
    assert response.status_code == 200
    assert "Test Hero" in str(response.data)

def test_get_heroes(client):
    response = client.get('/heroes')
    assert response.status_code == 200
    assert "Test Hero" in str(response.data)

def test_update_hero(client):
    test_hero = Hero(name="Test Hero", super_name="Test Superhero")
    db.session.add(test_hero)
    db.session.commit()
    response = client.put('/hero/1', json={"super_name": "Updated Superhero"})
    assert response.status_code == 200
    assert "Updated Superhero" in str(response.data)

def test_delete_hero(client):
    test_hero = Hero(name="Test Hero", super_name="Test Superhero")
    db.session.add(test_hero)
    db.session.commit()
    response = client.delete('/hero/1')
    assert response.status_code == 200
    assert "hero deleted successfully" in str(response.data)

# Similar test cases can be written for other routes (powers, hero_powers, etc.)

if __name__ == '__main__':
    pytest.main()
