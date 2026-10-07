# Task 04 - CI/CD Notes

I added a simple GitHub Actions workflow for this Docker project.

## What it does

1. Runs when code is pushed to `main` or a pull request targets `main`.
2. Sets up Python 3.12 and installs the project dependencies.
3. Runs flake8 for a basic code check.
4. Runs the unit tests with pytest.
5. Builds the Docker image after linting and tests pass.
6. On a push to `main`, the image is pushed to GitHub Container Registry (GHCR).

The workflow uses the GitHub-provided `GITHUB_TOKEN` for the GHCR login, so no password or token is written in the YAML file.

## Main workflow file

`.github/workflows/ci-cd.yml`

## Image name

`ghcr.io/<github-username>/rabtech-task-03-docker`
