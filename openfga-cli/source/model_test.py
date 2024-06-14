import unittest
import asyncio
from model import write_authorization_model
from store import create_store, delete_store


class TestAuthorizationModel(unittest.TestCase):

    def test_write_authorization_model(self):
        store = asyncio.run(create_store("store"))

        # read file model.json and convert it to json
        with open('/home/app/openfga-cli/source/model.json', 'r') as file:
            json_model = file.read()

        asyncio.run(write_authorization_model(store['id'], json_model))
        # assert response is True

        # asyncio.run(delete_store(store['id']))
