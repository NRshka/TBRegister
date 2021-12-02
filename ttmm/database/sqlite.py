"""Manager to apply common operations on sqlite database.

Using aiosqlite to make it asynchronously."""
import os
import aiosqlite
import asyncio
from typing import Dict, List, Union

from .abstract import AbstractDatabase


class SQLiteManager(AbstractDatabase):
    def __init__(self, database_connection):
        self.conn = database_connection
        self.conn.row_factory = aiosqlite.Row
        asyncio.create_task(self.init_table())

    async def init_table(self):
        await self.conn.execute(
            """CREATE TABLE IF NOT EXISTS projects(id integer primary key autoincrement, project_name text);"""
        )

    async def get_project_signature(self, project_name: str):
        table_cur = await self.conn.execute(f"""SELECT * FROM {project_name};""")
        return [description[0] for description in table_cur.description]

    async def get_project_models_list(self, project_name: str):
        result: List[Dict[str, Union[str, int, float]]] = []
        column_names = await self.get_project_signature(project_name)

        cursor = await self.conn.execute(f"""SELECT * FROM {project_name};""")
        data = await cursor.fetchall()

        for entry in data:
            data_dict = {}

            for column_name, value in zip(column_names, entry):
                data_dict[column_name] = value

            result.append(data_dict)

        await cursor.close()

        return result, column_names

    async def add_project(self, project_name: str, tags: List[str]):
        # check if this projectname already exists
        cursor = await self.conn.execute(
            """SELECT * FROM projects WHERE project_name = '{project_name}';"""
        )
        project = await cursor.fetchone()

        if project:
            raise ValueError(f"{project_name} is already exists!")

        await cursor.execute(
            f"""INSERT INTO projects (project_name) VALUES ('{project_name}');"""
        )
        tags_values = ", ".join([f"{tag_name} text" for tag_name in tags])
        await cursor.execute(f"""CREATE TABLE {project_name} (id int, {tags_values});""")

        await self.conn.commit()
        await cursor.close()

    async def delete_project(self, project_name: str):
        await self.conn.execute(
            f"""DELETE FROM projects WHERE project_name = {project_name};"""
        )
        await self.conn.execute(f"""DROP TABLE {project_name};""")
        await self.conn.commit()

    async def update_project(
        self,
        project_name: str,
        names_to_add: List[str],
        names_to_drop: List[str],
        names_to_rename: Dict[str, str],
    ):
        for orig_name, new_name in names_to_rename.items():
            await self.conn.execute(
                f"""ALTER TABLE {project_name} RENAME {orig_name} TO {new_name};"""
            )

        for name_to_delete in names_to_drop:
            await self.conn.execute(
                f"""ALTER TABLE {project_name} DROP {name_to_delete};"""
            )

        for name_to_append in names_to_add:
            await self.conn.execute(f"""ALTER TABLE {project_name} ADD {name_to_append};""")

        await self.conn.commit()

    def close_connection(self):
        asyncio.create_task(self.conn.close())

    async def get_projects_list(self) -> List[str]:
        cursor = await self.conn.execute("""SELECT project_name FROM projects;""")
        projects = await cursor.fetchall()

        return [project[0] for project in projects]


async def init_sqlite_database_manager_in_context(app):
    database_path = os.getenv("DATABASE_PATH")
    assert database_path, RuntimeError("DATABASE_PATH must be set in environment")

    database_connection = await aiosqlite.connect(database_path)
    manager = SQLiteManager(database_connection)
    app["DB"] = manager

    yield

    await database_connection.close()
