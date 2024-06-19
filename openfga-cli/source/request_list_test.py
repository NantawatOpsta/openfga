import asyncio
import unittest
from store import create_store, delete_store
from model import write_authorization_model
from request import RequestWrite, RequestList
# from request import RequestListUser


class TestRequestList(unittest.TestCase):

    def test_get_list_tenant_admin_can_access(self):
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
            "user:admin1",
            "member",
            "group:admin"
        ))

        asyncio.run(RequestWrite(
            store.id,
            model.authorization_model_id,
            "group:admin#member",
            "can_view",
            "tenant:tenant1"
        ))

        asyncio.run(RequestWrite(
            store.id,
            model.authorization_model_id,
            "group:admin#member",
            "can_view",
            "tenant:tenant2"
        ))

        asyncio.run(RequestWrite(
            store.id,
            model.authorization_model_id,
            "group:admin#member",
            "can_view",
            "tenant:tenant3"
        ))

        list_of_tenants = asyncio.run(RequestList(
            store.id,
            model.authorization_model_id,
            "user:admin1",
            "can_view",
            "tenant"
        ))

        self.assertEqual(len(list_of_tenants.objects), 3)
        self.assertIn("tenant:tenant1", list_of_tenants.objects)
        self.assertIn("tenant:tenant2", list_of_tenants.objects)
        self.assertIn("tenant:tenant3", list_of_tenants.objects)

        # delete the store
        asyncio.run(delete_store(store.id))

    def test_get_list_project_indirect_relation(self):
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
            "user:admin1",
            "member",
            "group:admin"
        ))

        asyncio.run(RequestWrite(
            store.id,
            model.authorization_model_id,
            "group:admin#member",
            "can_view",
            "project:project1"
        ))

        asyncio.run(RequestWrite(
            store.id,
            model.authorization_model_id,
            "group:admin#member",
            "can_view",
            "project:project2"
        ))

        asyncio.run(RequestWrite(
            store.id,
            model.authorization_model_id,
            "group:admin#member",
            "can_view",
            "project:project3"
        ))

        list_of_projects = asyncio.run(RequestList(
            store.id,
            model.authorization_model_id,
            "user:admin1",
            "can_view",
            "project"
        ))

        self.assertEqual(len(list_of_projects.objects), 3)
        self.assertIn("project:project1", list_of_projects.objects)
        self.assertIn("project:project2", list_of_projects.objects)
        self.assertIn("project:project3", list_of_projects.objects)

        # delete the store
        asyncio.run(delete_store(store.id))

    # def test_list_member_in_tenant(self):
    #     # create a store
    #     store = asyncio.run(create_store("store"))

    #     # read file model.json and convert it to json
    #     with open('/home/app/openfga-cli/source/model.json', 'r') as file:
    #         json_model = file.read()

    #     # write the authorization model to the store
    #     model = asyncio.run(write_authorization_model(store.id, json_model))

    #     asyncio.run(RequestWrite(
    #         store.id,
    #         model.authorization_model_id,
    #         "user:admin1",
    #         "member",
    #         "group:admin"
    #     ))

    #     asyncio.run(RequestWrite(
    #         store.id,
    #         model.authorization_model_id,
    #         "user:admin2",
    #         "member",
    #         "group:admin"
    #     ))

    #     asyncio.run(RequestWrite(
    #         store.id,
    #         model.authorization_model_id,
    #         "user:admin3",
    #         "member",
    #         "group:admin"
    #     ))

    #     asyncio.run(RequestWrite(
    #         store.id,
    #         model.authorization_model_id,
    #         "group:admin#member",
    #         "can_view",
    #         "tenant:tenant1"
    #     ))

    #     # list_of_members = asyncio.run(RequestListUser(
    #     #     store.id,
    #     #     model.authorization_model_id,
    #     #     "can_view",
    #     #     "tenant",
    #     #     "tenant1"
    #     # ))

    #     # list_of_members = RequestListUser(
    #     #     store.id,
    #     #     model.authorization_model_id,
    #     #     "can_view",
    #     #     "tenant",
    #     #     "tenant1"
    #     # )

    #     # self.assertEqual(len(list_of_members.objects), 3)

    #     # delete the store
    #     asyncio.run(delete_store(store.id))
