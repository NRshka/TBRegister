import logging
import os
import asyncio
from aiohttp import web
from .server import router


@router.post("/upload")
async def upload_file(request: web.Request) -> web.Response:
    file_storage_path = os.getenv("FILE_STORAGE_PATH")
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

    models_count = db_manager.get_models_count(theme)
    filedir_path = os.path.join(file_storage_path, theme, filename)

    if not os.path.isdir(filedir_path):
        try:
            os.mkdir(filedir_path)
        except OSError as err:
            logging.error(f"Could not create directory {filedir_path}:" + str(err))
            return web.HTTPBadRequest()

    filepath = os.path.join(filedir_path, str(models_count))

    with open(filepath, 'wb') as file:
        while True:
            chunk = await file_container_field.read()
            if not chunk:
                break

            await file.write(chunk)

    asyncio.create_task(
        db_manager.add_model(theme, filename, filepath, tags)
    )

    return web.Response()
