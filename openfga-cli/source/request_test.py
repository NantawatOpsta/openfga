import asyncio
import unittest
from store import create_store, delete_store
from model import write_authorization_model
from request import WriteRequestUser


class TestRelation(unittest.TestCase):

    # add user1 tenant1 can view only tenant1
    # add user2 tenant2 can view only tenant2
    # add admin to admin_group can view all
    def test_add_user_project_relation(self):
        # create a store
        store = asyncio.run(create_store("store"))

        # read file model.json and convert it to json
        with open('/home/app/openfga-cli/source/model.json', 'r') as file:
            json_model = file.read()

        # write the authorization model to the store
        model = asyncio.run(write_authorization_model(store.id, json_model))

        # write the user project relation to the store
        asyncio.run(WriteRequestUser(
            store.id,
            model.authorization_model_id,
            "user:user1",
            "member",
            "tenant:tenant1"
        ))

        # delete the store
        asyncio.run(delete_store(store.id))
