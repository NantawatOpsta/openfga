from client import get_openfga_client
from openfga_sdk.client.models.tuple import ClientTuple
from openfga_sdk.client.models.write_request import ClientWriteRequest
from openfga_sdk.client.models.check_request import ClientCheckRequest
from openfga_sdk.client.models.list_objects_request import ClientListObjectsRequest


async def WriteRequestCreate(
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


async def WriteRequestDelete(
        store_id, authorization_model_id, user, relation, obj
):
    client = get_openfga_client(
        store_id=store_id, authorization_model_id=authorization_model_id
    )

    options = {
        "authorization_model_id": authorization_model_id
    }

    body = ClientWriteRequest(
        deletes=[
            ClientTuple(
                user=user,
                relation=relation,
                object=obj,
            )
        ]
    )

    return await client.write(body, options)


async def WriteRequestCheck(
    store_id, authorization_model_id, user, relation, obj
):
    client = get_openfga_client(
        store_id=store_id, authorization_model_id=authorization_model_id
    )

    options = {
        "authorization_model_id": authorization_model_id
    }

    body = ClientCheckRequest(
        user=user,
        relation=relation,
        object=obj
    )

    return await client.check(body, options)


async def WriteRequestList(
    store_id, authorization_model_id, user, relation, type_name
):
    client = get_openfga_client(
        store_id=store_id, authorization_model_id=authorization_model_id
    )

    options = {
        "authorization_model_id": authorization_model_id
    }

    body = ClientListObjectsRequest(
        user=user,
        relation=relation,
        type=type_name
    )

    return await client.list_objects(body, options)