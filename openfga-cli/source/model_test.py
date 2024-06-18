import unittest
import asyncio
from model import write_authorization_model, read_latest_authorization_model
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

    def test_read_latest_authorization_model(self):
        # create a store
        store = asyncio.run(create_store("store"))

        # read file model.json and convert it to json
        with open('/home/app/openfga-cli/source/model.json', 'r') as file:
            json_model = file.read()

        # write the authorization model to the store
        model = asyncio.run(write_authorization_model(store.id, json_model))

        # get the latest authorization model
        get_model = asyncio.run(read_latest_authorization_model(store.id))

        assert get_model.authorization_model.id == model.authorization_model_id

        # delete the store
        asyncio.run(delete_store(store.id))