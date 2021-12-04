import os
import asyncio
from aiohttp import web
from .server import router


@router .post("/upload")
async def upload_file(request: web.Request) -> web.Response:
    theme = request.query.get("theme")
    db_manager = request.config_dict["DB"]

    multipart_reader = await request.multipart()
    filename = None
    file_container_field = None
    tags = {}

    while True:
        field = await multipart_reader.next()
        if not field:
            break
        elif field.name == 'filename':
            filename = (await field.read()).decode('utf-8')
        elif field.name == 'file':
            file_container_field = field
        else:
            tags[field.name] = (await field.read()).decode('utf-8')

    if not (filename and file_container_field and theme):
        return web.HTTPBadRequest()

    asyncio.create_task(db_manager.add_model(
        theme, filename, '', tags
    ))

    return web.Response()
