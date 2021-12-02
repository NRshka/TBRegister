from typing import List
import os
import pytest
import asyncio

from ttmm.database import init_sqlite_database_manager_in_context


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session", autouse=True)
async def database_manager():
    os.environ["DATABASE_PATH"] = "test.db"
    cfg = {}

    async for _ in init_sqlite_database_manager_in_context(cfg):
        yield cfg["DB"]

    os.remove("test.db")


async def create_project(database_manager, project_name: str, tags: List[str]):
    await database_manager.add_project(project_name, tags)


@pytest.mark.asyncio
async def test_creating_project(database_manager):
    project_name = "project_name"
    tags = ["tag1", "tag2", "tag3"]

    await create_project(database_manager, project_name, tags)

    signature = await database_manager.get_project_signature(project_name)

    assert signature == ['id'] + tags


@pytest.mark.asyncio
async def test_getting_projects_list(database_manager):
    project_names = ["project1", "project2"]
    await create_project(database_manager, project_names[0], ["tag1"])
    await create_project(database_manager, project_names[1], ["tag2"])

    projects_list = await database_manager.get_projects_list()

    difference = set(project_names).difference(projects_list)

    assert len(difference) == 0, f"Expected no difference between created and received projects, but {difference}"
