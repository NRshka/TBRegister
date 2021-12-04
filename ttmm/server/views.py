import aiohttp_jinja2
from aiohttp import web
from .server import router


@router.get("/")
@aiohttp_jinja2.template("index.html")
def index(request: web.Request) -> web.Response:
    return {}


@router.get("/projects")
@aiohttp_jinja2.template("projects.html")
async def projects_list_page(request: web.Request):
    db_manager = request.config_dict["DB"]
    project_names = await db_manager.get_projects_list()

    return {"projects": project_names}


@router.get("/models")
@aiohttp_jinja2.template("models.html")
async def models_list(request: web.Request):
    project_name = request.query["project"]
    assert project_name, web.HTTPNotFound()

    db_manager = request.config_dict["DB"]
    models_info, column_names = await db_manager.get_project_models_list(project_name)

    return {"models": models_info, "project_names": project_name, "column_names": column_names}
