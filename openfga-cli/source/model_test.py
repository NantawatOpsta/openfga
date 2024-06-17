import unittest
import asyncio
from model import write_authorization_model
from store import create_store, delete_store


class TestAuthorizationModel(unittest.TestCase):

    def test_write_authorization_model(self):
        # create a store
        store = asyncio.run(create_store("store"))

        # read file model.json and convert it to json
        with open('/home/app/openfga-cli/source/model.json', 'r') as file:
            json_model = file.read()

        # write the authorization model to the store
        asyncio.run(write_authorization_model(store.id, json_model))

        # delete the store
        asyncio.run(delete_store(store.id))
