from dataclasses import dataclass
import logging
import os
import pathlib
from typing import Literal, Optional
from pulumi import automation as auto
from pydantic import BaseModel


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


class LocalWorkspaceConfiguration(BaseModel):
    work_dir: str
    stack_name: str
    project_name: Optional[str] = None
    action: Literal["preview", "up", "destroy"] = "preview"


def run(config: LocalWorkspaceConfiguration):
    if config.work_dir is None:
        raise ValueError("work_dir must be set")

    # if config.backend_url is None:
    #     raise ValueError("backend_url must be set")

    work_dir = config.work_dir

    stack = auto.create_or_select_stack(
        stack_name=config.stack_name,
        project_name=config.project_name,
        work_dir=str(INFRA_FOLDER_PATH / work_dir)
    )

    region = stack.get_config("aws:region")
    logging.info(
        f"Current AWS region: {region.value if region else 'not set'}")
    stack.set_config("aws:region", auto.ConfigValue(value="us-east-1"))
    # stack.workspace.install_plugin("aws", "v7.16.0")

    if config.action == "up":
        result = stack.up(on_output=print)
        return result.summary
    elif config.action == "preview":
        result = stack.preview(on_output=print)
        return result.change_summary
    elif config.action == "destroy":
        result = stack.destroy(on_output=print)
        stack.workspace.remove_stack(config.stack_name)
        return result.summary
    else:
        raise ValueError(f"Unknown action: {config.action}")
