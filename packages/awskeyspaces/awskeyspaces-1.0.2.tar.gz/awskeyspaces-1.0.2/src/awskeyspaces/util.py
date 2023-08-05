#!/usr/bin/env/ python
"""
    AWS KEYSPACE CONNECTOR UTIL
"""
import os

from cassandra.cqlengine import management

from .connection import connect

__all__ = ["migrate", "run_migrate", "create_ksp", "proxydb"]

_models_to_migrate = set()


def migrate(cls):
    """
    migrate(ModelA)
    add tables for sync
    """
    _models_to_migrate.add(cls)


@connect
def run_migrate():
    """
    migrate(ModelA)
    migrate(ModelB)

    run_migrate()
    # connect once
    """
    os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"
    for model in _models_to_migrate:
        management.sync_table(model, keyspaces=[os.getenv("CLUSTER_KSP")])


@connect
def create_ksp(keyspace=None):
    if (ksp := keyspace) is None:
        ksp = os.getenv("CLUSTER_KSP")

    os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"
    management.create_keyspace_simple(ksp, 1)


@connect
def proxydb():
    """
    initialize connection with cassandra
    """
    return True
