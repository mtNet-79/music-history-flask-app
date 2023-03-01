import pytest
import json
from flask import Flask, current_app
from flaskr import create_app, db
from flask_wtf.csrf import generate_csrf
from config import TestingConfig
from flaskr.models import Composer, Performer, Title
from flaskr.forms import ComposerForm


@pytest.fixture(scope="module")
def test_client():
    app = create_app(test_config=True)
    app_context = app.app_context()
    app_context.push()
    db.create_all()

    yield app.test_client()

    db.session.remove()
    db.drop_all()
    app_context.pop()


class TestComposer:
    new_composer = {
        "name": "Johann Sebastian Bach",
        "year_born": 1685,
        "year_deceased": 1750,
        "nationality": "Germany"
    }
    
    
    def test_show_form(client):
        response = client.get('/composers/create')

        assert response.status_code == 200
        assert b'Add Composer' in response.data

    def test_create_composer(self, test_client):
        """Test add new composer"""
        # res = test_client.post("/composers/create", json=self.new_composer)
        # data = json.loads(res.data)
        form = ComposerForm()
        form.name.data = 'Mozart'
        form.born.data = '1756-01-27'
        form.deceased.data = '1791-12-05'
        form.nationality.data = 'Austrian'
        # use Flask-WTF to generate a CSRF token for the form
        csrf_token = generate_csrf()
        response = test_client.post('/composers/create', data={
            'csrf_token': csrf_token,
            **form.data  # use the form data dictionary to populate the request data
        })
        
        # print(f"ON CREATE COMPOSER DATA is {data}")

        # assert res.status_code == 200
        # assert data["success"] == True
        # assert data["created"]
        # assert len(data["composers"]) > 0
        assert response.status_code == 200
        assert json.loads(response.data)['success'] is True
        assert json.loads(response.data)['created'] is not None
        assert json.loads(response.data)['composers'] is not None
        assert json.loads(response.data)['total_Composers'] is not None
        
    def test_create_composer_failure(client):
        """Add Composer Fail"""
        response = client.post('/composers/create', data={})

        assert response.status_code == 400
        assert json.loads(response.data)['success'] is False
        
    def test_get_composer(self, test_client):
        """Test retrieve composer"""
        res = test_client.get("/composers")
        data = json.loads(res.data)

        assert res.status_code == 200
        assert len(data['composers']) > 0

    def test_get_composer_by_id(self, test_client):
        """Test retrieve composer by id"""
        composer = Composer(
            name="Wolfgang Amadeus Mozart",
            year_born=1756,
            year_deceased=1791,
            nationality="Austria"
        )
        composer.insert()

        res = test_client.get(f"/composers/{composer.id}")
        data = json.loads(res.data)

        assert res.status_code == 200
        assert data["success"] == True


    def test_delete_composer(self, test_client):
        """Test delete composer by id"""
        composer = Composer(
            name="Wolfgang Amadeus Mozart",
            year_born=1756,
            year_deceased=1791,
            nationality="Austria"
        )
        composer.insert()

        res = test_client.delete(f"/composers/{composer.id}")
        data = json.loads(res.data)
        # print(f"IN DELETE CO<MPOSER DATA IS {data}")

        assert res.status_code == 200
        assert data["success"] == True
        assert data["deleted"] == composer.id

    
class TestPerformer:
    new_performer = {
        "name": "Glen Gould",
        "year_born": 1932,
        "year_deceased": 1982,
        "nationality": "Canadian",
        "rating": 4.5
    }

    def test_create_performer(self, test_client):
        """ Test create new performer record"""
        res = test_client.post("/performers/create", json=self.new_performer)
        data = json.loads(res.data)

        assert res.status_code == 200
        assert data["success"] == True
        assert data["created"]
        assert len(data["performers"]) > 0

    def test_retrieve_performer(self, test_client):
        """ Test retrieve performer"""
        res = test_client.get("/performers")
        data = json.loads(res.data)
        # print(f"GET PERFORMER data {data}")
        assert res.status_code == 200
        assert len(data['performers']) > 0
        
    def test_get_performer_by_id(self, test_client):
        """ Test retrieve performer by id"""
        
        title1 = Title(
            name="conductor"                
        )
        
        title1.insert()
        title2 = Title(
            name="flautist"
        )
        title2.insert()

        performer = Performer(
            name="Béla Drahos",
            year_born=1955,
            nationality="Hungary",
            titles=[title1, title2]
            
        )
        

        performer.insert()
        res = test_client.get(f"/performers/{performer.id}")
        data = json.loads(res.data)

        assert res.status_code == 200
        assert data["success"] == True

    def test_delete_performer(self, test_client):
        """ Test delete performer """
        title1 = Title(
            name="conductor"                
        )
        
        title1.insert()
        title2 = Title(
            name="flautist"
        )
        title2.insert()

        performer = Performer(
            name="Béla Drahos",
            year_born=1955,
            nationality="Hungary",
            titles=[title1, title2]
            
        )
        

        performer.insert()
        print(f"FOR MY DELETE TEST the ID IS {performer.id}")
        res = test_client.delete(f"/performers/{performer.id}")
        data = json.loads(res.data)

        assert res.status_code == 200
        assert data["success"] == True
        assert data["deleted"] == performer.id
