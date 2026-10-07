# RabTech Academy - Task 03

## Multi-Stage Docker Containerization & Optimization

I made a small Python Flask web app for this task. It uses PostgreSQL for storing notes and Redis as a second service.

### What is included

- `Dockerfile` - multi-stage build
- `docker-compose.yml` - web + PostgreSQL + Redis
- `app.py` - simple Flask app
- `.dockerignore` - keeps unwanted files out of the image
- `BUILD_LOG_COMMANDS.md` - commands used to produce the build/health logs

### Main points of the task

1. The Dockerfile uses a builder stage and a separate runtime stage.
2. The application runs as `appuser` instead of root.
3. Compose starts the web app, PostgreSQL and Redis.
4. Health checks are added for the web app, PostgreSQL and Redis.
5. PostgreSQL and Redis use named volumes so data is kept when containers are recreated.

### How I tested it locally

Run:

```bash
docker compose up --build -d
```

Open:

`http://localhost:5000`

Health check:

```bash
curl http://localhost:5000/health
```

Check containers:

```bash
docker compose ps
```

Check the web image size:

```bash
docker image ls
```

The task asks for a final image below 150 MB. This should be checked on the machine where the image is built, because the exact size depends on the base image and Docker build environment.

### Volume persistence test

1. Add a note on the web page.
2. Run `docker compose down`.
3. Run `docker compose up -d`.
4. Open the page again and check that the note is still there.

The PostgreSQL named volume is what keeps the database data between these container restarts/recreates.

### Note

Build logs are intentionally generated on the local Docker machine rather than being made up in advance. The exact output, image ID and size should come from the actual build.
