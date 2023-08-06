import boto3
import json
from botocore.exceptions import ClientError
from django.core.exceptions import ImproperlyConfigured


def get_secret(secret_name: str, region_name: str) -> dict:
    """Gets a text secret from AWS Secrets Manager. This function currently doesn't handle binary secrets.

    It attempts to use the instance or task credentials.

    :param secret_name: The name of the secret
    :param region_name: The region where the secret is stored
    :return: The dictionary representation of the secret
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
        return json.loads(secret_value["SecretString"])
    raise ImproperlyConfigured("The specified secret doesn't contain any text.")
