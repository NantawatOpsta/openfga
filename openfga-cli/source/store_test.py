import unittest
import asyncio
from store import create_store, get_store, delete_store


class TestStore(unittest.TestCase):

    def test_create_get_delete_store(self):
        # create store
        response = asyncio.run(create_store("store"))
        assert response['name'] == "store"
        assert response['id'] is not None

        # get store
        response = asyncio.run(get_store(store_id=response['id']))
        assert response['name'] == "store"
        assert response['id'] is not None

        # delete store
        response = asyncio.run(delete_store(store_id=response['id']))
        assert response is True
