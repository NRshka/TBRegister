import pytest

from ttmm.database import SQLiteManager


@pytest.fixture(scope="session", autouse=True)
def database_manager():
    manager = SQLiteManager('test.db')
    yield manager


@pytest.mark.asyncio
async def test_creating_project(database_manager):
    project_name = 'project_name'
    tags = ['tag1', 'tag2', 'tag3']

    await database_manager.add_project(project_name, tags)
    signature = await database_manager.get_project_signature(project_name)

    assert signature == ['id'] + tags
