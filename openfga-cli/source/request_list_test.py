import asyncio
import unittest
from store import create_store, delete_store
from model import write_authorization_model
from request import RequestWrite, RequestDelete, RequestCheck


class TestRequestList(unittest.TestCase):

    def test_create_delete(self):
        # create a store
        store = asyncio.run(create_store("store"))

        # read file model.json and convert it to json
        with open('/home/app/openfga-cli/source/model.json', 'r') as file:
            json_model = file.read()

        # write the authorization model to the store
        model = asyncio.run(write_authorization_model(store.id, json_model))

        asyncio.run(RequestWrite(
            store.id,
            model.authorization_model_id,
            "user:admin",
            "member",
            "group:admin"
        ))

        asyncio.run(RequestDelete(
            store.id,
            model.authorization_model_id,
            "user:admin",
            "member",
            "group:admin"
        ))

        # delete the store
        asyncio.run(delete_store(store.id))
