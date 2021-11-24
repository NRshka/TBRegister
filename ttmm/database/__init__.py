"""Module for handling database connections and requests.

Any database manager should implement AbstractDatabase interface."""
from .sqlite import SQLiteManager, init_sqlite_database_manager_in_context

__all__ = ["SQLiteManager", "init_sqlite_database_manager_in_context"]
