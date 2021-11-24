import aiohttp_jinja2
from aiohttp import web
from .server import router


@router.get("/")
@aiohttp_jinja2.template("index.html")
def index(request: web.Request) -> web.Response:
    return {}
