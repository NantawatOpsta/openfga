import asyncio
import unittest
from store import create_store, delete_store
from model import write_authorization_model
from request import RequestWrite, RequestList
from request import RequestListUser, RequestListUserJson, RequestListRelations


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

    def test_list_member_in_tenant(self):
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
            "user:admin2",
            "member",
            "group:admin"
        ))

        asyncio.run(RequestWrite(
            store.id,
            model.authorization_model_id,
            "user:admin3",
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

        list_of_members = asyncio.run(RequestListUser(
            store.id,
            model.authorization_model_id,
            "can_view",
            "tenant",
            "tenant1"
        ))
        assert len(list_of_members.users) == 3

        list_of_members = RequestListUserJson(
            store.id,
            model.authorization_model_id,
            "can_view",
            "tenant",
            "tenant1"
        )
        assert len(list_of_members['users']) == 3

        # delete the store
        asyncio.run(delete_store(store.id))

    def test_list_user_relations(self):
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
            "can_edit",
            "tenant:tenant1"
        ))

        asyncio.run(RequestWrite(
            store.id,
            model.authorization_model_id,
            "group:admin#member",
            "can_add",
            "tenant:tenant1"
        ))

        list_of_relations = asyncio.run(RequestListRelations(
            store.id,
            model.authorization_model_id,
            "user:admin1",
            ["can_view", "can_edit", "can_add"],
            "tenant:tenant1"
        ))

        assert len(list_of_relations) == 3
        assert "can_view" in list_of_relations
        assert "can_edit" in list_of_relations
        assert "can_add" in list_of_relations

        # delete the store
        asyncio.run(delete_store(store.id))
