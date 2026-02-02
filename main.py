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
    backend_url: str = typer.Option(
        default="", envvar="PULUMI_BACKEND_URL", help="Backend URL for the Pulumi project"),
):
    from automation.cli import run
    from automation.cli import LocalWorkspaceConfiguration
    config = LocalWorkspaceConfiguration(
        work_dir=work_dir,
        project_name=project_name,
        stack_name=stack_name,
        action=action,
        backend_url=backend_url,
    )
    print(run(config))


if __name__ == "__main__":
    app()
