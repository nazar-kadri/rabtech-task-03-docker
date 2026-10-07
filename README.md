[README_with_task4.md](https://github.com/user-attachments/files/33151099/README_with_task4.md)
# RabTech Academy - Task 03

## Multi-Stage Docker Containerization & Optimization

I made a small Python Flask web app for this task. It uses PostgreSQL and Redis as supporting services.

## What is included

- Dockerfile - multi-stage Docker build
- docker-compose.yml - web app, PostgreSQL and Redis
- app.py - simple Flask web app
- requirements.txt - Python packages used by the app
- .dockerignore - files not needed in the Docker build

## Main points

- Uses a builder stage and a separate runtime stage.
- The app runs as a non-root user.
- PostgreSQL and Redis run as separate services.
- Health checks are included.
- PostgreSQL and Redis use named volumes for data persistence.

## How to run

```bash
docker compose up --build -d
```

Then open:

http://localhost:5000

Health check:

```bash
curl http://localhost:5000/health
```

Check running containers:

```bash
docker compose ps
```

## Volume test

1. Add a note in the app.
2. Run `docker compose down`.
3. Run `docker compose up -d`.
4. Check that the note is still there.

## Note

Build logs and final image size should be taken from the actual local Docker build. I have not added fake build output.

## Task 04 - CI/CD

[![CI/CD](https://github.com/nazar-kadri/rabtech-task-03-docker/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/nazar-kadri/rabtech-task-03-docker/actions/workflows/ci-cd.yml)

I added a simple GitHub Actions workflow for this project. It runs on pull requests and pushes to `main`.

- Sets up Python 3.12 and installs dependencies.
- Runs a basic flake8 check.
- Runs unit tests with pytest.
- Builds the Docker image after the checks pass.
- On a push to `main`, pushes the image to GitHub Container Registry.
- Uses the GitHub provided `GITHUB_TOKEN` for registry login instead of putting a token in the workflow file.

Workflow file: `.github/workflows/ci-cd.yml`
