"""Manager to apply common operations on sqlite database.

Using aiosqlite to make it asynchronously."""
import aiosqlite
import asyncio
from typing import Dict, List, Union

from .abstract import AbstractDatabase


class SQLiteManager(AbstractDatabase):
    def __init__(self, database_path: str):
        self.loop = asyncio.get_event_loop()

        self.database_path = database_path
        self.conn = self.loop.run_until_complete(aiosqlite.connect(self.database_path))
        self.cursor = self.loop.run_until_complete(self.conn.cursor())
        self.loop.run_until_complete(self.init_table())

    async def init_table(self):
        await self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS projects(id int primary key, project_name text);"""
        )

    async def get_project_signature(self, project_name: str):
        table_cur = await self.conn.execute(f"""SELECT * FROM {project_name};""")
        return [description[0] for description in table_cur.description]

    async def get_project_models_list(self, project_name: str):
        result: List[Dict[str, Union[str, int, float]]] = []
        column_names = self.get_project_signature(project_name)

        await self.cursor.execute(f"""SELECT * FROM {project_name};""")
        data = await self.cursor.fetchall()

        for entry in data:
            data_dict = {}

            for column_name, value in zip(column_names, entry):
                data_dict[column_name] = value

            result.append(data_dict)

        return result

    async def add_project(self, project_name: str, tags: List[str]):
        # check if this projectname already exists
        await self.cursor.execute(
            """SELECT * FROM projects WHERE project_name = '{project_name}';"""
        )
        project = await self.cursor.fetchone()

        if project:
            raise ValueError(f"{project_name} is already exists!")

        await self.cursor.execute(
            f"""INSERT INTO projects (project_name) VALUES ('{project_name}');"""
        )
        tags_values = ", ".join([f"{tag_name} text" for tag_name in tags])
        await self.cursor.execute(f"""CREATE TABLE {project_name} (id int, {tags_values});""")

    async def delete_project(self, project_name: str):
        await self.cursor.execute(
            f"""DELETE FROM projects WHERE project_name = {project_name};"""
        )
        await self.cursor.execute(f"""DROP TABLE {project_name};""")

    async def update_project(
        self,
        project_name: str,
        names_to_add: List[str],
        names_to_drop: List[str],
        names_to_rename: Dict[str, str],
    ):
        for orig_name, new_name in names_to_rename.items():
            await self.cursor.execute(
                f"""ALTER TABLE {project_name} RENAME {orig_name} TO {new_name};"""
            )

        for name_to_delete in names_to_drop:
            await self.cursor.execute(
                f"""ALTER TABLE {project_name} DROP {name_to_delete};"""
            )

        for name_to_append in names_to_add:
            await self.cursor.execute(f"""ALTER TABLE {project_name} ADD {name_to_append};""")

    def close_connection(self):
        self.loop.run_until_complete(self.conn.close())
