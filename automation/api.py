from typing import Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from automation.cli import LocalWorkspaceConfiguration


class LocalWorkspaceSchema(BaseModel):
    work_dir: str
    project_name: str
    stack_name: str
    action: Literal["preview", "up", "destroy"] = "preview"


fastapi_app = FastAPI()


@fastapi_app.get("/healthz")
def healthz():
    return {"status": "ok"}


@fastapi_app.post("/local-workspace/run")
def run_local_workspace(
    request: LocalWorkspaceSchema
):
    from automation.cli import run

    try:
        config = LocalWorkspaceConfiguration(
            **request.model_dump()
        )
        result = run(config)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
