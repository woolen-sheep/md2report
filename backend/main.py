import pathlib
from typing import Dict
import uuid
import os
from zipfile import ZipFile
from tempfile import TemporaryFile

from pydantic import BaseModel

from config.config import load_config, server_config

from fastapi import Depends, FastAPI, HTTPException, UploadFile, status, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from celery import Celery
from celery.result import AsyncResult
import aiofiles

from md2report import convert_md_to_docx

celery = Celery("tasks")
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")  # type: ignore
celery.conf.result_backend = os.environ.get(  # type: ignore
    "CELERY_RESULT_BACKEND", "redis://localhost:6379/0"
)
celery.conf.broker_transport_options = {"visibility_timeout": 3600}


@celery.task
def create_convert_task(args: Dict) -> str:
    conf = load_config(args=args)
    return convert_md_to_docx(conf)


app = FastAPI()

# allow the origin of local frontend
origins = [
    "http://192.168.2.230:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api")


class CreateTaskParam(BaseModel):
    # name of template to use.
    # templates are defined in `config/config.yaml`
    template: str = "HUST"
    # if enable highlight
    highlight: bool = True


@router.get("/healthz")
async def health_check():
    return {"message": "Hello World"}


@router.post("/tasks")
async def convert_markdown(file: UploadFile, param: CreateTaskParam = Depends()):
    """
    Create a generate taskself.

    The markdown file (or extracted file) will be palced in a `cache_path`.
    Then a celery task will be created to process the file(s).

    Params:
        file (UploadFile): The file need to be convert. Should be *.zip or *.md
        param (CreateTaskParam): params passed to worker, see `CreateTaskParam`
            for more info.
    """
    ext_name = file.filename.split(".")[-1]
    if ext_name != "zip" and ext_name != "md":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="please upload a .zip or .md file",
        )
    save_path = os.path.join(server_config.cache_path, uuid.uuid4().hex)
    os.makedirs(save_path)
    save_file = pathlib.Path(save_path).resolve() / "markdown.md"
    if ext_name == "zip":
        tmp_file = TemporaryFile()
        tmp_file.write(await file.read())
        with ZipFile(tmp_file) as zip:
            for fn in zip.namelist():
                extracted_path = pathlib.Path(zip.extract(fn, save_path))
                # TODO: ensure the behavior of zip files created on not-windows os.
                # convert encoding to gbk, to prevent garbled chars in filename.
                new_filename = os.path.join(save_path, fn.encode("cp437").decode("gbk"))
                extracted_path.rename(new_filename)
        # find the first markdown file
        # we assmue that there will be only one md file
        files = os.listdir(save_path)
        for f in files:
            if f.endswith(".md"):
                os.rename(os.path.join(save_path, f), str(save_file))
                break
    else:
        async with aiofiles.open(save_file, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)
    output_file = os.path.join(save_path, "output.docx")
    args = {"input": str(save_file), "output": output_file}
    args.update(param.dict())
    task = create_convert_task.delay(args)
    return JSONResponse({"task_id": task.id})


@router.get("/tasks/{task_id}/status")
def get_task_status(task_id):
    """
    Get celery task status.

    Note: if a task is not existed, the returned status
    will be `PENDING`.
    """
    task_result: AsyncResult = celery.AsyncResult(task_id)
    return JSONResponse({"status": task_result.status})


@router.get("/tasks/{task_id}")
def get_task_result(task_id):
    """
    Return the generated docx file when task is ready.
    """
    task_result: AsyncResult = celery.AsyncResult(task_id)
    if task_result.ready():
        return FileResponse(task_result.result, filename="output.docx")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="task pending or not existed"
    )


app.include_router(router)
