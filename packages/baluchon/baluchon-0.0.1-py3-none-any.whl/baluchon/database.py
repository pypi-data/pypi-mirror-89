from typing import Optional, Tuple, Dict, Any, Sequence

import pendulum
from clickhouse_driver import Client

from .constants import EMPTY_VERSION
from .exceptions import ConnectionNoSetException
from .validator import RaisingValidator
from .validator.schemas import DATABASE_CONFIG_SCHEMA, DSN_SCHEMA


class PatchedClient(Client):
    def __del__(self):
        self.disconnect()


class Database:
    def __init__(self, config: Dict[str, Any], dsn: Dict[str, Any]):
        """
        Args:
            config (dict): Configuration for migrations
            dsn (dict): The data source name for Clickhouse
        """
        validator = RaisingValidator()
        validator.validate(config, DATABASE_CONFIG_SCHEMA)
        self.config = validator.document
        validator = RaisingValidator()
        validator.validate(dsn, DSN_SCHEMA)
        self.dsn = validator.document
        self.client: Optional[Client] = None

    @property
    def db_name(self) -> str:
        return self.dsn["database"]

    @db_name.setter
    def db_name(self, value):
        self.dsn["database"] = value

    @property
    def replication(self) -> Optional[Dict[str, str]]:
        return self.config.get("replication")

    def open(self) -> None:
        """
        Create a new connection to Clickhouse and setup a new client.
        Required to query on the database

        Returns:
            None
        Example:
            self.open(dns={
                "database": "default",
                "host": "localhost",
                "port": "9000",
                "user": "default",
                "password": "password",
                "compression": True,
            })
        """

        self.client = PatchedClient(**self.dsn)

    def close(self) -> None:
        """
        Close and destroy the client
        Returns:
            None
        """
        if self.client is None:
            raise ConnectionNoSetException
        self.client.disconnect()
        self.client = None

    def run(self, query: str) -> Sequence[Tuple]:
        """
        Run a query on the database

        Args:
            query (str)
        Returns:
            list: List of rows as tuples
        """
        if self.client is None:
            raise ConnectionNoSetException
        return self.client.execute(str(query))

    def version(self) -> Tuple[int, bool]:
        """
        Give the currently active migration version

        Returns:
            int: The version
            bool: The dirty state.
        """
        query = (
            f"SELECT version, dirty FROM {self.db_name}.`{self.config['migration_table']}`"
            f" ORDER BY sequence DESC LIMIT 1;"
        )
        r = self.run(query)
        if not r:
            return EMPTY_VERSION, False
        return r[0][0], bool(r[0][1])

    def set_version(self, version: int, dirty: bool) -> None:
        """
        Set the migrations to a specific version
        Args:
            version (int)
            dirty (bool)
        Returns:
            None

        """
        assert type(version) is int, "Version must be an integer"
        assert type(dirty) is bool, "Dirty must be a boolean"
        query = (
            f"INSERT INTO {self.db_name}.`{self.config['migration_table']}` (version, dirty, sequence)"
            f" VALUES ({version}, {int(dirty)}, {int(pendulum.now('UTC').timestamp() * 1_000_000)});"
        )
        self.run(query)

    def ensure_version_table(self) -> None:
        """
        Checks if versions table exists and, if not, creates it.
        """
        query = (
            f"SHOW TABLES FROM {self.db_name} LIKE '{self.config['migration_table']}';"
        )
        self.run(query)
        fields = """
        (
            version  Int64,
            dirty    UInt8,
            sequence UInt64
        )
        """
        if self.replication:
            parameters = [
                self.replication["zoo_path"],
                self.replication["replica_name"],
            ]
            if self.replication.get("other_parameters"):
                parameters.append(self.replication["other_parameters"])
            parameters_string = ",".join(f"'{s}'" for s in parameters)
            query = f"""
                    CREATE TABLE IF NOT EXISTS {self.db_name}.`schema_migrations` ON CLUSTER {self.replication['cluster_name']}
                    {fields}
                    ENGINE = ReplicatedMergeTree({parameters_string})
                    ORDER BY version;
                """
        else:
            query = f"""
                CREATE TABLE IF NOT EXISTS `{self.config['migration_table']}`
                {fields}
                Engine=TinyLog
            """
        self.run(query)

    def drop(self) -> None:
        """
        Drop all tables in database
        TODO: will not work on dictionary
        """
        query = f"SHOW TABLES FROM {self.db_name}"
        r = self.run(query)
        for (table,) in r:
            query = f"DROP TABLE IF EXISTS {self.db_name}.{table};"
            self.run(query)
