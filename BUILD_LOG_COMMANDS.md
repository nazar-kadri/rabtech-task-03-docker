# Build / Health Log Commands

These are the commands I used/plan to use for the Task 03 proof. Run them in PowerShell or terminal from this folder.

## 1. Build the image

```bash
docker compose build --no-cache | Tee-Object -FilePath build-log.txt
```

## 2. Start the services

```bash
docker compose up -d | Tee-Object -FilePath run-log.txt
```

## 3. Check service health

```bash
docker compose ps | Tee-Object -FilePath health-log.txt
```

## 4. Check the application endpoint

```bash
curl http://localhost:5000/health
```

## 5. Check image size

```bash
docker images
```

## 6. Check that the app is not running as root

```bash
docker compose exec web id
```

The output should show the `appuser` account.

## 7. Persistence test

Add one note in the browser, then run:

```bash
docker compose down
docker compose up -d
```

Open the browser again and confirm the note is still present.

These logs should be committed to the repository after the commands have actually been run.
