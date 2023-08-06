import boto3
from botocore.exceptions import ClientError
from django.core.exceptions import ImproperlyConfigured


def get_secret(secret_name: str, region_name: str) -> str:
    """Gets a secret from AWS Secrets Manager.

    It attempts to use the instance or task credentials.

    The secret is returned as text, either as the base64 representation if it's a binary secret or as a json

    :param secret_name: The name of the secret
    :param region_name: The region where the secret is stored
    :return: The secret
    """
    session = boto3.session.Session(region_name=region_name)
    client = session.client(
        service_name="secretsmanager",
        region_name=region_name,
    )

    try:
        secret_value = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise ImproperlyConfigured("Failed to retrieve secret value.") from e

    if "SecretString" in secret_value:
        return secret_value["SecretString"]
    elif "SecretBinary" in secret_value:
        return secret_value["SecretBinary"]
    raise ImproperlyConfigured("The specified secret is malformed.")
