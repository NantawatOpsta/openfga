import asyncio
import unittest
from store import create_store, delete_store
from model import write_authorization_model
from request import RequestWrite, RequestDelete, RequestCheck, RequestList


class TestRelation(unittest.TestCase):

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

    # add user1 tenant1 can view only tenant1
    # add user2 tenant2 can view only tenant2
    def test_user_access_direct_check(self):
        # create a store
        store = asyncio.run(create_store("store"))

        # read file model.json and convert it to json
        with open('/home/app/openfga-cli/source/model.json', 'r') as file:
            json_model = file.read()

        # write the authorization model to the store
        model = asyncio.run(write_authorization_model(store.id, json_model))

        # write the user project relation to the store
        asyncio.run(RequestWrite(
            store.id,
            model.authorization_model_id,
            "user:user1",
            "member",
            "tenant:tenant1"
        ))

        asyncio.run(RequestWrite(
            store.id,
            model.authorization_model_id,
            "user:user2",
            "member",
            "tenant:tenant2"
        ))

        # check if user1 can view tenant1
        check_user_01 = asyncio.run(RequestCheck(
            store.id,
            model.authorization_model_id,
            "user:user1",
            "can_view",
            "tenant:tenant1"
        ))
        assert check_user_01.allowed is True

        # check if user2 can view tenant2
        check_user_02 = asyncio.run(RequestCheck(
            store.id,
            model.authorization_model_id,
            "user:user2",
            "can_view",
            "tenant:tenant2"
        ))
        assert check_user_02.allowed is True

        # delete the store
        asyncio.run(delete_store(store.id))

    # add admin to admin_group can view all
    def test_admin_group_check(self):
        # create a store
        store = asyncio.run(create_store("store"))

        # read file model.json and convert it to json
        with open('/home/app/openfga-cli/source/model.json', 'r') as file:
            json_model = file.read()

        # write the authorization model to the store
        model = asyncio.run(write_authorization_model(store.id, json_model))

        # write the admin to admin group
        asyncio.run(RequestWrite(
            store.id,
            model.authorization_model_id,
            "user:admin",
            "member",
            "group:admin"
        ))

        # write the admin group to can view all
        asyncio.run(RequestWrite(
            store.id,
            model.authorization_model_id,
            "group:admin#member",
            "can_view",
            "tenant:tenant1"
        ))

        # check if admin can view tenant1
        admin = asyncio.run(RequestCheck(
            store.id,
            model.authorization_model_id,
            "user:admin",
            "can_view",
            "tenant:tenant1"
        ))

        assert admin.allowed is True

        # delete the store
        asyncio.run(delete_store(store.id))
