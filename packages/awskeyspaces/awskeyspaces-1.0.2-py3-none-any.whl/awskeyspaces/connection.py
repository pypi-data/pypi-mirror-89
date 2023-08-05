#!/usr/bin/env/ python
"""
    AWS KEYSPACE CONNECTOR
"""
from functools import wraps
import os

from cassandra import ConsistencyLevel
from cassandra.policies import RoundRobinPolicy

from cassandra.cqlengine import connection
from cassandra.io.libevreactor import LibevConnection

from .auth import _auth_provider, _ssl_context

__all__ = ["connection", "get_session"]

_CLUSTER_HOST = os.getenv("CLUSTER_HOST", "127.0.0.1").split(",")
_CLUSTER_PORT = int(os.getenv("CLUSTER_PORT", 9142))


def connect(orig_function):
    """
    Decorator  connect to aws keypaces

    @connect
    def ....():
    """

    @wraps(orig_function)
    def wrapper(*args, **kwargs):
        connection.setup(
            hosts=_CLUSTER_HOST,
            ssl_context=_ssl_context,
            auth_provider=_auth_provider,
            port=_CLUSTER_PORT,
            load_balancing_policy=RoundRobinPolicy(),
            default_keyspace=os.getenv("CLUSTER_KSP"),
            protocol_version=4,
            lazy_connect=False,
            retry_connect=True,
            consistency=ConsistencyLevel.LOCAL_QUORUM,
            connection_class=LibevConnection,
        )
        return orig_function(*args, **kwargs)

    return wrapper


@connect
def get_session(name="default", keyspace=None):
    _session = connection.get_session(name)
    if keyspace:
        _session.set_keyspace(keyspace)
    return _session
