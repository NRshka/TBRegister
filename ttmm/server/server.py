from aiohttp import web
import aiohttp_jinja2
import jinja2

router = web.RouteTableDef()


def start_server(init_db_method, templates_path: str):
    app = web.Application()
    app.add_routes(router)
    app.cleanup_ctx.append(init_db_method)

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(templates_path))

    web.run_app(app)
