import unittest
import asyncio
from store import create_store, get_store, delete_store


class TestStore(unittest.TestCase):

    def test_create_get_delete_store(self):
        # create store
        store = asyncio.run(create_store("store"))
        assert store.name == "store"
        assert store.id is not None

        # get store
        store = asyncio.run(get_store(store_id=store.id))
        assert store.name == "store"
        assert store.id is not None

        # delete store
        store = asyncio.run(delete_store(store_id=store.id))
        assert store is True
