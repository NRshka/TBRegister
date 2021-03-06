import os
import logging
import ttmm.database as database
import ttmm.server as server


def main():
    logging.basicConfig(level=logging.DEBUG)
    os.environ["DATABASE_PATH"] = "test.db"

    server.start_server(
        database.init_sqlite_database_manager_in_context,
        "ttmm/server/templates"
    )


if __name__ == "__main__":
    main()
