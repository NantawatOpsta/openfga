from client import get_openfga_client
from openfga_sdk.client.models.tuple import ClientTuple
from openfga_sdk.client.models.write_request import ClientWriteRequest


async def WriteRequestUser(
        store_id, authorization_model_id, user, relation, obj
):
    client = get_openfga_client(
        store_id=store_id, authorization_model_id=authorization_model_id
    )

    options = {
        "authorization_model_id": authorization_model_id
    }

    body = ClientWriteRequest(
        writes=[
            ClientTuple(
                user=user,
                relation=relation,
                object=obj,
            )
        ]
    )

    return await client.write(body, options)
