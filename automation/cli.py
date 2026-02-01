import os
import pathlib
from pulumi import automation as auto
import subprocess
import argparse

parser = argparse.ArgumentParser(description="Pulumi Automation CLI")
parser.add_argument(
    "--action",
    choices=["up", "destroy", "preview"],
    required=True,
    default="preview",
    help="Action to perform: up, destroy, or preview"
)
parser.add_argument(
    "--stack",
    type=str,
    default="dev",
    help="Name of the Pulumi stack to operate on (default: dev)"
)
args = parser.parse_args()

ROOT_FOLDER_PATH = os.path.join(os.path.dirname(__file__), "..")
DATA_FOLDER_PATH = pathlib.Path(
    os.path.join(ROOT_FOLDER_PATH, "data")).resolve()

INFRA_FOLDER_PATH = pathlib.Path(
    os.path.join(ROOT_FOLDER_PATH, "infra")).resolve()


def run():
    work_dir = os.path.join(INFRA_FOLDER_PATH, "s3")

    stack = auto.create_or_select_stack(
        stack_name=args.stack,
        project_name="s3-sample-object",
        work_dir=os.path.join(INFRA_FOLDER_PATH, "s3"),
        opts=auto.LocalWorkspaceOptions(
            # support airgapped environments by specifying a custom pulumi home.
            # so we can cached plugins and avoid re-downloading on every run.
            # pulumi_home=os.path.join(ROOT_FOLDER_PATH, ".pulumi")
        )
    )

    # stack.workspace.install_plugin("aws", "v7.16.0")
    stack.set_config("aws:region", auto.ConfigValue(value="us-east-1"))

    if args.action == "up":
        result = stack.up(on_output=print)
        return result.summary
    elif args.action == "preview":
        result = stack.preview(on_output=print)
        return result.change_summary
    elif args.action == "destroy":
        result = stack.destroy(on_output=print)
        return result.summary
    else:
        raise ValueError(f"Unknown action: {args.action}")
