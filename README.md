# Development & Usage Guide

## 1. Using the Devcontainer

This project supports VS Code Dev Containers for a consistent development environment.

1. Open the project in VS Code.
2. When prompted, reopen in the container (or use the Command Palette: `Dev Containers: Reopen in Container`).
3. The environment will be set up automatically with all dependencies.

## 2. Build the Docker Image

From the project root, build the Docker image with:

```sh
docker build -t mypulumi:latest .
```

## 3. Run and Test the Built Docker Image

To run the Pulumi app in preview mode using the built image:
```sh
export PULUMI_BACKEND_URL=file://data
docker run --rm -it \
	--env-file ./.env \
	-v $(pwd)/infra/s3/data:/app/infra/s3/data \
	mypulumi:latest \
	uv run main.py --action preview
```

Replace `--action preview` with other actions as needed.

Note: by mounting the volume, we can keep local state backend. 
Otherwise, you state file will be lost between run.

---
For more details, see the inline comments in the Dockerfile and source code.
