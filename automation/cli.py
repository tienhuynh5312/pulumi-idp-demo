from dataclasses import dataclass
import os
import pathlib
from typing import Literal, Optional
from pulumi import automation as auto
# import subprocess
# import argparse

# parser = argparse.ArgumentParser(description="Pulumi Automation CLI")
# parser.add_argument(
#     "--action",
#     choices=["up", "destroy", "preview"],
#     default="preview",
#     help="Action to perform: up, destroy, or preview"
# )
# parser.add_argument(
#     "--stack",
#     type=str,
#     default="dev",
#     help="Name of the Pulumi stack to operate on (default: dev)"
# )
# args = parser.parse_args()

ROOT_FOLDER_PATH = os.path.join(os.path.dirname(__file__), "..")
DATA_FOLDER_PATH = pathlib.Path(
    os.path.join(ROOT_FOLDER_PATH, "data")).resolve()

INFRA_FOLDER_PATH = pathlib.Path(
    os.path.join(ROOT_FOLDER_PATH, "infra")).resolve()


@dataclass
class LocalWorkspaceConfiguration:
    project_name: str
    stack_name: str
    work_dir: Optional[str] = None
    backend_url: Optional[str] = None
    action: Literal["preview", "up", "destroy"] = "preview"

    def work_dir_program(self, subfolder_name: str) -> str:
        return str(INFRA_FOLDER_PATH / subfolder_name)


def run(config: LocalWorkspaceConfiguration):
    if config.work_dir is None:
        raise ValueError("work_dir must be set")

    if config.backend_url is None:
        raise ValueError("backend_url must be set")

    work_dir = config.work_dir

    stack = auto.create_or_select_stack(
        stack_name=config.stack_name,
        project_name=config.project_name,
        work_dir=config.work_dir,
        opts=auto.LocalWorkspaceOptions(
            # support airgapped environments by specifying a custom pulumi home.
            # so we can cached plugins and avoid re-downloading on every run.
            project_settings=auto.ProjectSettings(
                name=config.project_name,
                runtime="python",
                backend=auto.ProjectBackend(url=config.backend_url),
            ),
        )
    )

    # stack.workspace.install_plugin("aws", "v7.16.0")
    stack.set_config("aws:region", auto.ConfigValue(value="us-east-1"))

    if config.action == "up":
        result = stack.up(on_output=print)
        return result.summary
    elif config.action == "preview":
        result = stack.preview(on_output=print)
        return result.change_summary
    elif config.action == "destroy":
        result = stack.destroy(on_output=print)
        return result.summary
    else:
        raise ValueError(f"Unknown action: {config.action}")
