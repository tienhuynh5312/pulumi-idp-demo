# Development & Usage Guide
## Purpose
- Inspire by Crossplane implementation. Using Pulumi Automation API we can serve our infrastructure through API
and/or GitOps.
- A bit simpler than Crossplane since we don't need Kubernetes abeit we lose advantages of Kubernetes controller nature.

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
This is intended for local development using local state backend. Recommend running this
outside the devcontainer, prerably host or (WSL with docker integrated) since there is a problem
mouting folder inside devcontainer to host Docker and we are using Docker-in-Docker external mode
(expose host Docker to devcontainer)

Set .env file
```bash
cat << EOF > .env
AWS_ACCESS_KEY_ID=<DIY>
AWS_SECRET_ACCESS_KEY=<DIY>
AWS_SESSION_TOKEN=<DIY>
PULUMI_BACKEND_URL=file:///app/.pulumi/data
PULUMI_CONFIG_PASSPHRASE=<DIY>
PULUMI_HOME=/root/.pulumi
EOF
```

To run the Pulumi app in preview mode using the built image:
```sh
# LINUX
docker run --rm -it --env-file ./.env \
    -p 8000:8000 \
    -v ${PWD}/.pulumi:/app/.pulumi/data mypulumi:latest \
    uv run main.py local-workspace run \
    --work-dir /app/infra/s3 --action preview

docker run --rm -it --env-file ./.env  -v "${PWD}/.pulumi:/app/.pulumi/data" \
    -p 8000:8000 mypulumi:latest \
    uv run main.py local-workspace serve
```
```powershell
# WINDOWS
docker run --rm -it --env-file ./.env `
    -p 8000:8000 `
    -v ${PWD}/.pulumi:/app/.pulumi/data mypulumi:latest `
    uv run main.py local-workspace run `
    --work-dir /app/infra/s3 --action preview

docker run --rm -it --env-file ./.env  -v "${PWD}/.pulumi:/app/.pulumi/data" `
    -p 8000:8000 mypulumi:latest `
    uv run main.py local-workspace serve
```
---
Replace `--action preview` with other actions as needed.

Note: by mounting the volume, we can keep local state backend. 
Otherwise, you state file will be lost between run.

## 4. Local Testing with uv

You can run and test the Pulumi app directly in your devcontainer or local environment (without Docker) using `uv`:

```sh
uv run main.py local-workspace run --work-dir "$(pwd)/infra/s3/"
```

- This will execute the Pulumi automation locally, using the code and configuration in `infra/s3/`.
- Make sure your environment variables (such as AWS credentials and Pulumi config) are set, or use a `.env` file and a tool like `direnv` or `dotenv`.

You can pass additional arguments to `main.py` as needed for your workflow.

## 5. Pulumi Automation API Endpoint

This project exposes a FastAPI endpoint for running Pulumi operations programmatically.

### Endpoint

`POST /local-workspace/run`

**Request Body (JSON):**
- `work_dir` (str): Relative path to the Pulumi project directory (e.g., `"s3"`).
- `project_name` (str): Name of the Pulumi project (e.g., `"s3_sample_project"`).
- `stack_name` (str): Name of the Pulumi stack (e.g., `"dev"`).
- `action` (str): One of `"preview"`, `"up"`, or `"destroy"`.

**Example:**

```sh
curl -H "Content-Type: application/json" \
    -d '{"work_dir": "s3", "project_name": "s3_sample_project", "stack_name": "dev",  "action": "destroy"}' \
    "http://localhost:8000/local-workspace/run"
```

**Response:**
- On success: `{ "result": ... }`
- On error: `{ "error": "..." }`

This allows you to trigger Pulumi stack operations via HTTP, enabling integration with other tools or automation workflows.

---
For more details, see the inline comments in the Dockerfile and source code.
