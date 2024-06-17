from client import get_openfga_client
from openfga_sdk.models.create_store_request import CreateStoreRequest


async def create_store(name="Demo Store"):
    body = CreateStoreRequest(
        name=name,
    )

    client = get_openfga_client()
    response = await client.create_store(body)
    await client.close()
    return response


async def delete_store(store_id):
    client = get_openfga_client(store_id=store_id)
    await client.delete_store(options={})
    await client.close()
    return True


async def get_store(store_id):
    client = get_openfga_client(store_id=store_id)
    response = await client.get_store(options={})
    await client.close()
    return response
