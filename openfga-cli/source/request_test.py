import asyncio
import unittest
from store import create_store, delete_store
from model import write_authorization_model
from request import WriteRequestCreate, WriteRequestDelete, WriteRequestCheck, WriteRequestList


class TestRelation(unittest.TestCase):

    def test_create_delete(self):
        # create a store
        store = asyncio.run(create_store("store"))

        # read file model.json and convert it to json
        with open('/home/app/openfga-cli/source/model.json', 'r') as file:
            json_model = file.read()

        # write the authorization model to the store
        model = asyncio.run(write_authorization_model(store.id, json_model))

        asyncio.run(WriteRequestCreate(
            store.id,
            model.authorization_model_id,
            "user:admin",
            "member",
            "admin_group:admin"
        ))

        asyncio.run(WriteRequestDelete(
            store.id,
            model.authorization_model_id,
            "user:admin",
            "member",
            "admin_group:admin"
        ))

        # delete the store
        asyncio.run(delete_store(store.id))

    # add user1 tenant1 can view only tenant1
    # add user2 tenant2 can view only tenant2
    # add admin to admin_group can view all
    def test_user_check(self):
        # create a store
        store = asyncio.run(create_store("store"))

        # read file model.json and convert it to json
        with open('/home/app/openfga-cli/source/model.json', 'r') as file:
            json_model = file.read()

        # write the authorization model to the store
        model = asyncio.run(write_authorization_model(store.id, json_model))

        # write the user project relation to the store
        asyncio.run(WriteRequestCreate(
            store.id,
            model.authorization_model_id,
            "user:user1",
            "member",
            "tenant:tenant1"
        ))

        asyncio.run(WriteRequestCreate(
            store.id,
            model.authorization_model_id,
            "user:user2",
            "member",
            "tenant:tenant2"
        ))

        asyncio.run(WriteRequestCreate(
            store.id,
            model.authorization_model_id,
            "user:admin",
            "member",
            "admin_group:admin"
        ))

        # check if user1 can view tenant1
        check_user_01 = asyncio.run(WriteRequestCheck(
            store.id,
            model.authorization_model_id,
            "user:user1",
            "can_view",
            "tenant:tenant1"
        ))
        assert check_user_01.allowed is True

        # check if user2 can view tenant2
        check_user_02 = asyncio.run(WriteRequestCheck(
            store.id,
            model.authorization_model_id,
            "user:user2",
            "can_view",
            "tenant:tenant2"
        ))
        assert check_user_02.allowed is True

        # check if user2 can view tenant2
        admin = asyncio.run(WriteRequestCheck(
            store.id,
            model.authorization_model_id,
            "user:admin",
            "can_view",
            "tenant:tenant1"
        ))
        # assert admin.allowed is True
        print(admin)

        admin_relate = asyncio.run(WriteRequestList(
            store.id,
            model.authorization_model_id,
            "user:user1",
            "can_view",
            "tenant"
        ))

        print(admin_relate)

        # delete the store
        # asyncio.run(delete_store(store.id))
