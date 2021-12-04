from typing import Dict, List, Union
import os
import pytest
import asyncio

from ttmm.database import init_sqlite_database_manager_in_context


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session", autouse=True)
async def database_manager():
    os.environ["DATABASE_PATH"] = ":memory:"
    cfg = {}

    async for _ in init_sqlite_database_manager_in_context(cfg):
        yield cfg["DB"]


async def create_project(database_manager, project_name: str, tags: List[str]):
    await database_manager.add_project(project_name, tags)


@pytest.mark.asyncio
async def test_creating_project(database_manager):
    project_name = "project_name"
    tags = ["tag1", "tag2", "tag3"]

    await create_project(database_manager, project_name, tags)

    signature = await database_manager.get_project_signature(project_name)

    assert signature == ["id", "filename", "filepath"] + tags


@pytest.mark.asyncio
async def test_getting_projects_list(database_manager):
    project_names = ["project1", "project2"]
    await create_project(database_manager, project_names[0], ["tag1"])
    await create_project(database_manager, project_names[1], ["tag2"])

    projects_list = await database_manager.get_projects_list()

    difference = set(project_names).difference(projects_list)

    assert len(difference) == 0, f"Expected no difference between created and received projects, but {difference}"


async def add_file_to_database(
    database_manager,
    project_name: str,
    filename: str,
    filepath: str,
    tags: Dict[str, Union[str, int, float]]
):
    await database_manager.add_model(project_name, filename, filepath, tags)


@pytest.mark.asyncio
async def test_adding_model(database_manager):
    project_name = "project"
    filename = "filename"
    filepath = "filepath"
    tags = {"tag1": "value1", "tag2": "value2", "tag3": "value3"}

    await create_project(database_manager, project_name, list(tags.keys()))

    await add_file_to_database(
        database_manager,
        project_name, 
        filename,
        filepath,
        tags
    )

    models, _ = await database_manager.get_project_models_list(project_name)

    assert models[0]["filename"] == filename
    assert models[0]["filepath"] == filepath
    assert all(models[0][tag] == value for tag, value in tags.items())
