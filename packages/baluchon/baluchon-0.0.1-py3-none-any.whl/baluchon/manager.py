import logging
from typing import Sequence, Tuple

from .database import Database
from .constants import EMPTY_VERSION
from .exceptions import (
    DirtyVersionException,
    NoChangeException,
    InvalidVersionException,
    NoMigrationException,
    ShortLimitException,
)
from .migration import Migration
from .source import Source

logger = logging.getLogger(__name__)


class MigrationManager:
    def __init__(
        self,
        database: Database,
        source: Source,
        graceful_stop: bool = True,
    ):
        self.source = source
        self.database = database
        self.graceful_stop = graceful_stop

        self.database.open()
        self.source.open()

        self.database.ensure_version_table()

    def close(self) -> None:
        """
        Close closes the source and the database.

        Returns:
            None
        """
        logger.info("Closing source and database...")
        self.database.close()
        self.source.close()

    def migrate(self, version: int) -> None:
        """
        Migrate looks at the currently active migration version,
        then migrates either up or down to the specified version.

        Args:
            version (int): The specified version

        Returns:
            None
        """
        assert type(version) is int, "Version must be an integer"
        current_version, dirty = self.database.version()
        if dirty:
            raise DirtyVersionException(current_version)
        migrations = self.read(start=current_version, dest=version)
        self.run_migrations(migrations=migrations)

    def steps(self, n) -> None:
        """
        Looks at the currently active migration and
        migrate up if n > 0, and down if n < 0.

        Args:
            n: Number of steps. Can be positive or negative

        Returns:
            None
        """
        assert type(n) is int, "The step must be an integer"
        if n == 0:
            raise NoChangeException
        current_version, dirty = self.database.version()
        from pprint import pprint

        if dirty:
            raise DirtyVersionException(current_version)
        if n > 0:
            migrations = self.read_up(start=current_version, limit=n)
        else:
            migrations = self.read_down(start=current_version, limit=-n)
        self.run_migrations(migrations=migrations)

    def up(self) -> None:
        """
        Looks at the currently active migration version
        and migrate all the way up (applying all up migrations).

        Returns:
            None
        """
        current_version, dirty = self.database.version()
        if dirty:
            raise DirtyVersionException(current_version)
        migrations = self.read_up(start=current_version)
        self.run_migrations(migrations=migrations)

    def down(self) -> None:
        """
        Looks at the currently active migration version
        and migrate all the way down (applying all down migrations).

        Returns:
            None
        """
        current_version, dirty = self.database.version()
        if dirty:
            raise DirtyVersionException(current_version)
        migrations = self.read_down(start=current_version)
        self.run_migrations(migrations=migrations)

    def drop(self) -> None:
        """
        Drop deletes everything in the database.

        Returns:
            None

        """
        self.database.drop()

    # Steps, Up or Down instead.
    def run(self, migration: Migration) -> None:
        """
        Run a migration into the database

        Args:
            migration (Migration): the Migration object

        Returns:
            None
        """
        assert isinstance(migration, Migration), "migration must be a Migration object"
        current_version, dirty = self.database.version()
        if dirty:
            raise DirtyVersionException(current_version)
        self.run_migrations([migration])

    def force(self, version: int) -> None:
        """
        Sets to a migration version without checking the currently active version.
        It resets the dirty state to false.

        Args:
            version (int): The specified version

        Returns:
            None
        """
        assert type(version) is int, "Version must be an integer"
        if version < -1:
            raise InvalidVersionException
        self.database.set_version(version=version, dirty=False)

    def version(self) -> Tuple[int, bool]:
        """
        Returns the currently active migration version.

        Returns:
            int: The version
            bool: The dirty state
        """

        return self.database.version()

    def version_exists(self, version: int) -> bool:
        """
        Checks the source if either the up or down migration
        for the specified migration version exists.

        Args:
            version (int)

        Returns:

        """
        assert type(version) is int, "Version must be an integer"
        try:
            self.source.read_query_up(version)
            self.source.read_query_down(version)
        except NoMigrationException:
            return False
        return True

    def get_migration(self, version: int, target_version: int) -> Migration:
        """
        Create the Migration object that will go for `version` to `target_version`

        Args:
            version (int):
            target_version (int):

        Returns:
            Migration
        """

    def read(self, start, dest) -> Sequence[Migration]:
        """
        Reads either up or down migrations from source `start` to `dest`.

        Args:
            start (int):
            dest (int):

        Returns:
            list: Sequence of Migration
        """
        assert type(start) is int, "Start version must be an integer"
        assert type(dest) is int, "Destination version must be an integer"

        # Check if version exists
        if start >= 0 and not self.version_exists(start):
            raise NoMigrationException(f"Missing migration for version {start}")
        if dest >= 0 and not self.version_exists(dest):
            raise NoMigrationException(f"Missing migration for version {dest}")
        if start == dest:
            raise NoChangeException
        # Up migration
        migrations = []
        if start < dest:
            if start == EMPTY_VERSION:
                # Apply first migration
                first_migration = self.source.first()
                migrations.append(first_migration)
                start = first_migration.version
            while start < dest:
                next_migration = self.source.next(start)
                migrations.append(next_migration)
                start = next_migration.version
        else:
            while start > dest and start >= 0:
                prev_migration = self.source.prev(start)
                migrations.append(prev_migration)
                start = prev_migration.version
        return migrations

    def read_up(self, start: int, limit=None) -> Sequence[Migration]:
        assert type(start) is int, "Start version must be an integer"
        assert limit is None or type(limit) is int, "Limit version must be an integer"
        """
        Reads up migrations from `start` limited by `limit`.
        If `limit` is not provided it will read until there are no more migrations.

        Args:
            start: The starting version
            limit (int)(optional): toto

        Returns:
            list: Sequence of Migration
        """
        # Check if version exists
        if start >= 0 and not self.version_exists(start):
            raise NoMigrationException(f"Missing migration for version {start}")

        if limit == 0:
            raise NoChangeException

        count = 0
        migrations = []
        while True:
            if start == EMPTY_VERSION:
                print("empty")
                # Apply first migration
                first_migration = self.source.first()
                migrations.append(first_migration)
                start = first_migration.target_version
                count += 1
            else:
                try:
                    next_migration = self.source.next(start)
                    migrations.append(next_migration)
                    start = next_migration.target_version
                    count += 1
                except NoMigrationException:
                    # Check if no migrations has been applied
                    if limit is None and count == 0:
                        raise NoChangeException
                    # Check if end has been reached without limit
                    if limit is None:
                        return migrations
                    # Check if end has been reached without applying any migrations
                    if limit > 0 and count == 0:
                        raise NoChangeException
                    # Check if end has been reached but limit was too short
                    if count < limit:
                        raise ShortLimitException(limit)

            if limit is not None and count >= limit:
                break
        return migrations

    def read_down(self, start, limit=None) -> Sequence[Migration]:
        """
        Reads down migrations from `start` limited by `limit`.
        If `limit` is not provided it will read until there are no more migrations.

        Args:
            start: The starting version
            limit (int)(optional): toto

        Returns:
            list: Sequence of Migration
        """
        if start == EMPTY_VERSION:
            raise NoChangeException
        # Check if version exists
        if start >= 0 and not self.version_exists(start):
            raise NoMigrationException(f"Missing migration for version {start}")

        if limit == 0:
            raise NoChangeException
        count = 0
        migrations = []
        while True:
            try:
                prev_migration = self.source.prev(start)
                migrations.append(prev_migration)
                start = prev_migration.target_version
                count += 1
            except NoMigrationException:
                # Check if there is no limit or limit was not reached, we then unapply the first migration
                if limit is None or limit > count:
                    first_migration = self.source.first(direction="down")
                    migrations.append(first_migration)
                    return migrations
                # Check if end has been reached but limit was too short
                if count < limit:
                    raise ShortLimitException(limit)

            if limit is not None and count >= limit:
                break
            count += 1
        return migrations

    def run_migrations(self, migrations: Sequence[Migration]) -> None:
        """
        Will run a sequence of migrations on the database

        Args:
            migrations (list): Sequence of the migrations to run

        Returns:
            None
        """
        for migration in migrations:
            # Set version on dirty state
            self.database.set_version(version=migration.target_version, dirty=True)
            if migration.query:
                logger.info(f"Reading and executing {migration.execution_string()} ...")
                self.database.run(migration.query)
            # Set to clean state
            self.database.set_version(version=migration.target_version, dirty=False)
            logger.info(f"Finished {migration.execution_string()}")
