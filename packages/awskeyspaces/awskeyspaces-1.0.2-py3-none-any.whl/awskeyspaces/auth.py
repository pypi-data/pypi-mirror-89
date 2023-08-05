"""
    AWS KEYSPACE AUTH PROVIDER

"""
import os

from ssl import SSLContext, PROTOCOL_TLSv1_2, CERT_REQUIRED
from cassandra.auth import PlainTextAuthProvider


__all__ = ["_auth_provider", "_ssl_context"]

AWS_CERT_PEM = f"{os.path.dirname(__file__)}/AmazonRootCA1.pem"

_ssl_context = SSLContext(PROTOCOL_TLSv1_2)
_ssl_context.load_verify_locations(f"{AWS_CERT_PEM}")
_ssl_context.verify_mode = CERT_REQUIRED

_auth_provider = PlainTextAuthProvider(
    username=os.getenv("CLUSTER_USER"),
    password=os.getenv("CLUSTER_PASS"),
)
