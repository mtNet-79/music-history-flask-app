import unittest
# import pytest
import json
from sqlalchemy import func
from flaskr import create_app, db
from flask import Flask, current_app
from config import TestingConfig
from flaskr.models import Composer, Performer, Title


class ComposerTestCase(unittest.TestCase):
    """Configure database connection"""

    def setUp(self):
        self.app = create_app(test_config=True)
        self.client = self.app.test_client

        self.new_composer = {
            "name": "Johann Sebastian Bach",
            "year_born": 1685,
            "year_deceased": 1750,
            "nationality": "Germany"
        }
        # with self.app.app_context():
        #     assert current_app == self.app
        #     self.db.create_all()
        with self.app.app_context():
            # db.create_all()
            assert current_app == self.app

            composer = Composer(
                name="Wolfgang Amadeus Mozart",
                year_born=1756,
                year_deceased=1791,
                nationality="Austria"
            )

            composer.insert()

            self.del_id = Composer.query.all()[0].id

    def tearDown(self):
        with self.app.app_context():
            # print(f"tear down {Composer.query.all()[0].id}")
            if Composer.query.all()[0].id:
                res = self.client().delete(
                    "/composers/"+str(Composer.query.all()[0].id))

    def test_create_composer(self):
        """ Test add new composer"""
        res = self.client().post("/composers/create", json=self.new_composer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["composers"]))

    def test_get_composer(self):
        """ Test retrieve composer"""
        res = self.client().get("/composers")
        data = json.loads(res.data)
        print(f"GET COMPOSER data {data}")
        self.assertEqual(res.status_code, 200, msg='{0}'.format({res}))
        self.assertTrue(len(data['composers']))

    def test_get_composer_by_id(self):
        res = self.client().get(f"/composers/{self.del_id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_composer(self):
        """ Test delete composer """
        res = self.client().delete("/composers/"+str(self.del_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200, msg='{0}'.format(res))
        self.assertEqual(data["success"], True)
        self.assertTrue(data["deleted"])


class PerformerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(test_config=True)
        self.client = self.app.test_client

        self.new_performer = {
            "name": "Glen Gould",
            "year_born": 1932, 
            "year_deceased": 1982,
            "nationality": "Canadian",
            "rating": 4.5
        }
        # with self.app.app_context():
        #     assert current_app == self.app
        #     self.db.create_all()
        with self.app.app_context():
            assert current_app == self.app
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

            self.del_id = Performer.query.all()[0].id

    def tearDown(self):
        pass
        # with self.app.app_context():
        #     # print(f"tear down {Composer.query.all()[0].id}")
        #     if Performer.query.all()[0].id:
        #         res = self.client().delete(
        #             "/performers/"+str(Performer.query.all()[0].id))

    def test_create_performer(self):
        res = self.client().post("/performers/create", json=self.new_performer)
        data = json.loads(res.data)
        print(f"TEST CREATE P data {data}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["performers"]))

    def test_get_performer(self):
        """ Test retrieve performer"""
        res = self.client().get("/performers")
        data = json.loads(res.data)
        print(f"GET PERFORMER data {data}")
        self.assertEqual(res.status_code, 200, msg='{0}'.format({res}))
        self.assertTrue(len(data['performers']))

    def test_get_composer_by_id(self):
        res = self.client().get(f"/performers/{self.del_id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_performer(self):
        """ Test delete performer """
        res = self.client().delete("/performers/"+str(self.del_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200, msg='{0}'.format(res))
        self.assertEqual(data["success"], True)
        self.assertTrue(data["deleted"])
 

if __name__ == "__main__":
    unittest.main()
