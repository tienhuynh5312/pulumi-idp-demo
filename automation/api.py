from inspect import stack
from typing import Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from automation.cli import LocalWorkspaceConfiguration, INFRA_FOLDER_PATH
from pulumi import automation as auto
from automation.cli import run


fastapi_app = FastAPI()


@fastapi_app.get("/healthz")
def healthz():
    return {"status": "ok"}


@fastapi_app.get("/infra/local/{work_dir}")
def list_local_stacks(
        work_dir: str):

    work_dir = work_dir

    ws = auto.LocalWorkspace(work_dir=str(INFRA_FOLDER_PATH / work_dir))
    ws_stacks = ws.list_stacks(include_all=True)

    return {"stacks": ws_stacks}


@fastapi_app.post("/infra/local/{work_dir}/{stack_name}/{action}")
def run_local_workspace(
    work_dir: str,
    stack_name: str,
    action: Literal["preview", "up", "destroy"] = "preview"
):
    try:
        config = LocalWorkspaceConfiguration(
            work_dir=work_dir,
            stack_name=stack_name,
            action=action
        )
        result = run(config)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
