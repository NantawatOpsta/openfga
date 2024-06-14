import json
from client import get_openfga_client


async def write_authorization_model(store_id, json_model):
    client = get_openfga_client(store_id=store_id)
    await client.write_authorization_model(json.loads(json_model))
    await client.close()
