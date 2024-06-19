import os
import openfga_sdk
from openfga_sdk.client import OpenFgaClient
from openfga_sdk.configuration import RetryParams


def get_openfga_api_url():
    return os.environ.get('FGA_API_URL')


def get_openfga_client(
        store_id=os.environ.get('FGA_STORE_ID'),
        authorization_model_id=os.environ.get('FGA_MODEL_ID')
):
    configuration = openfga_sdk.ClientConfiguration(
        api_url=get_openfga_api_url(),
        retry_params=RetryParams(max_retry=3, min_wait_in_ms=250)
    )
    if store_id:
        configuration.store_id = store_id
    if authorization_model_id:
        configuration.authorization_model_id = authorization_model_id
    return OpenFgaClient(configuration)
