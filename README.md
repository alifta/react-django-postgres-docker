# Home In Block

## Dev

### Annotation

```python
# * Importnant (Green)
# ! Deprecated (Red)
# ? Should (Blue)
# TODO: (Orange)

```

## Frontend - React

### Porject setup

1. Create docker container and install react via `Vite`:

```shell
docker run --rm -it -v $(pwd):/code -w /code node:22.12.0 sh -c "npm create vite@latest frontend -- --template react && cd frontend/ && npm install"
```

2. Create `.dockerignore` file.

3. Create docker file for frontend container `Dockerfile.frontend`:

```dockerfile
FROM node

COPY ./frontend /frontend
RUN rm -rf /frontend/node_modules

WORKDIR /frontend
RUN npm ci

CMD [ "npm", "run", "dev" ]
```

4. Create docker compose file for fronend service in `docker-compose.yaml` file:

```yaml
services:
    frontend:
        build:
            context: .
            dockerfile: Dockerfile.frontend
        ports:
            - "5173:5173"
        develop:
            watch:
                - action: sync
                  path: ./frontend
                  target: /frontend
                  ignore:
                      - node_modules
```

5. Modify Vite config file `vite.config.js`:

```js
export default defineConfig({
	plugins: [react()],
	server: { host: "0.0.0.0" },
});
```

6.  Build and start container in watch mode:

```shell
docker compose up --watch --build
```

7. Sync docker to local development folder. The `watch` is one way sync from local folder to container, but if we want to sync back an installed package on the cointaner back to our local folder, we can use:

```shell
docker compose run --rm -v $(pwd)/frontend:/frontend frontend sh -c "npm install axios"
```

8. Restart the fronend server in the cointaner, after installing a new package, we can stop the server with (control+c) and then re-build with:

```shell
docker compose build
```

and then finally run the new built in watch mode:

```shell
docker compose up --watch
```

# Backend

## Django

### Environment management

To export the installed Python libraries, we normally export them into `requirements.txt` file. The following setup is the base requirement for backend which is `Django`.

Create the requirement file `requirements.txt`:

```text
Django==5.1.4
```

### Create admin user

To create an admin user for Django (enabaling access to admin portal) for the Django project runnning on docker is by using the following command:

```shell
docker compose run --rm backend sh -c "python manage.py createsuperuser"
```

### Run Django tests

```shell
docker compose run --rm backend sh -c "python manage.py test"
```

### Run Django scripts

```shell
docker compose run --rm backend sh -c "python manage.py runscript orm_script"
```

### Run Django commands

```shell
docker compose run --rm backend sh -c "python manage.py create_data"
```

## Docker

### Complite docker

To complie the docer files after modifying one of them, run the following command:

```shell
docker compose build
```

### Run docker and re-run if changed

To run dcoker and bring up the services in terminal, run the new built docker files afrer "Build" command, eun them in watch mode:

```shell
docker compose up --watch
```

### Stop docker

```shell
docker compose down
```

### Dockerfile for backend

To create `Dockerfile.backend` you can use the following for basic reference:

```

FROM python:3.13

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./backend /backend
WORKDIR /backend

RUN python -m venv env /py && \
 /py/bin/pip install --upgrade pip && \
 /py/bin/pip install -r /requirements.txt

ENV PATH="/py/bin:$PATH"

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

```

However, the most update to date is saved at `./requirements.dev.txt` address in this project.

### Docker Compose

To add a new service to `docker-compose.yaml` file consider the following as a base example for Django backend service:

```yaml
backend:
    build:
        context: .
        dockerfile: Dockerfile.backend
    ports:
        - "8000:8000"
    volumes:
        - ./backend:/backend
```

However, the most update to date is saved at `./docker-compose.yml` for development envirnonment or `./docker-compose-deploy.yml` for production environment's address in this project.

### Test container

To Test to see whether the container and dockerfile runs without any error by using:

```shell
docker build .
```

### Run a command in Django container

To run a command in Django container we use `docker compose run --rm backend sh -c "django-admin startproject backend .""`

For example we can install a new Django on a container directly by using as a the step in project setup:

```shell
docker compose run --rm backend sh -c "django-admin startproject <backend> ."
docker compose run --rm backend sh -c "python manage.py startapp core"
docker-compose run --rm backend sh -c "python manage.py createsuperuser"
```

You can replace `backend` with `app` for example.

### Dockerignore

To create the `.dockerignore` file, the following can be the base case for frontend service:

```text
README.md
frontend/node_modules/
```

## Dev

### Create a local Python environment

To get a better code experience in local develpment usising VScode, it is usual to install Django locally in a isolated env by using the following commands in terminal:

```shell
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Database

### Run DB Migration

To run a database migration in Django in container run the following:

```shell
docker compose run --rm backend sh -c "python manage.py makemigrations"
docker compose run --rm backend sh -c "python manage.py migrate"
```

### Connect to DB running on the docker container from terminal

```shell
docker compose exec db psql -U user -d db
```

### Remove "db" database from psql terminal

Need to first switch to a different database such as `postgres`, and then delete (drop) the `db` database.

```psql
\c postgres
DROP DATABASE db WITH (FORCE);
CREATE DATABASE db;
```

### Reset database migration history

`core` is the name of the Django app that the `migrations` folder live in.

```
python manage.py migrate --fake core zero
```

### Force create new initial migrations

After using two prevous steps and this, a new databse should be created, and avoid issues from database migrations (only use in dev).

```
python manage.py makemigrations --name initial core
```

### Port 5432 (on local machine) is not available

This error indicates that that port 5432 is already in use. To resolve, we first find the service using this port number and then we terminate it

```bash
sudo lsof -i :5432
sudo kill -9 <PID>
```

## Radis

### Troubleshoot Redis

shows logs from Rdius service.

```shell
docker compose run --rm redis sh -c "redis-server --loglevel debug"
```

## Celery

### Troubleshoot Celery Worker

```shell
docker compose run --rm redis sh -c "celery -A backend worker -l info"
```
