import pytest

from ttmm.database import SQLiteManager


@pytest.fixture()
def database_manager():
    return SQLiteManager('test.db')


def test_creating_project(database_manager):
    project_name = 'project_name'
    tags = ['tag1', 'tag2', 'tag3']

    database_manager.add_project(project_name, tags)
    signature = database_manager.get_project_signature(project_name)

    assert signature == ['id'] + tags
