from baluchon.constants import DEFAULT_MIGRATIONS_TABLE

DATABASE_CONFIG_SCHEMA = {
    "migration_table": {
        "required": True,
        "type": "string",
        "default": DEFAULT_MIGRATIONS_TABLE,
    },
    "replication": {
        "type": "dict",
        "schema": {
            "cluster_name": {"required": True, "type": "string"},
            "zoo_path": {"required": True, "type": "string"},
            "replica_name": {"required": True, "type": "string"},
            "other_parameters": {"type": "string"},
        },
    },
}

DSN_SCHEMA = {
    "database": {"required": True, "type": "string"},
    "host": {"required": True, "type": "string"},
    "port": {"required": True, "type": "string"},
    "user": {"required": True, "type": "string"},
    "password": {"required": True, "type": "string"},
    "compression": {"type": "boolean"},
}

SQL_FOLDER_SOURCE_SCHEMA = {
    "folder": {"required": True, "type": "string"},
    "context": {
        "type": "dict",
        "allow_unknown": True,
        "default": None
    },
}
