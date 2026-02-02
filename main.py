from typing import Literal
import typer
import os

app = typer.Typer()
local_workspace = typer.Typer()
app.add_typer(local_workspace, name="local-workspace")


@local_workspace.command("run")
def run(
    work_dir: str = typer.Option(
        help="Working directory for the Pulumi project"),
    project_name: str = typer.Option(
        default="s3-sample-object", help="Name of the Pulumi project"),
    stack_name: str = typer.Option(
        default="dev", help="Name of the Pulumi stack"),
    action: Literal["preview", "up", "destroy"] = typer.Option(
        default="preview", help="Action to perform: up, destroy, or preview"),
    # backend_url: str = typer.Option(
    #     default="", envvar="PULUMI_BACKEND_URL", help="Backend URL for the Pulumi project", show_envvar=True),
):
    from automation.cli import run
    from automation.cli import LocalWorkspaceConfiguration

    config = LocalWorkspaceConfiguration(
        work_dir=work_dir,
        project_name=project_name,
        stack_name=stack_name,
        action=action
    )
    print(run(config))


@local_workspace.command("serve")
def serve(
    host: str = typer.Option("0.0.0.0", help="Host to bind the server to"),
    port: int = typer.Option(8000, help="Port to bind the server to"),
):
    """Serve a FastAPI endpoint for local workspace operations."""
    import uvicorn
    from automation.api import fastapi_app

    uvicorn.run(fastapi_app, host=host, port=port)


if __name__ == "__main__":
    app()
