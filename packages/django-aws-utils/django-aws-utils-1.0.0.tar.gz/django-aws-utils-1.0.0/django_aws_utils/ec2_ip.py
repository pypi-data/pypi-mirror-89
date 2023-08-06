import requests
from django.core.exceptions import ImproperlyConfigured


def get_ec2_ip() -> str:
    """Get the machine's IP as used by the load balancer.

    The result should be added to ALLOWED_HOSTS to prevent Django from returning HTTP500.
    For example, in your `settings.py`:


    .. code-block::

        ALLOWED_HOSTS = [
            get_ec2_ip(),
            "app.example.com"
        ]


    For the time being, this only supports the Metadata Version 1.

    :return: A string containing the instance's IPv4
    """
    endpoint = "http://169.254.169.254/latest/meta-data/local-ipv4"
    try:
        # Use a short timeout, the metadata endpoint should answer quickly
        return requests.get(endpoint, timeout=2.0).text
    except Exception as e:
        raise ImproperlyConfigured("Failed to retrieve IPv4 from EC2 instance metadata.") from e
