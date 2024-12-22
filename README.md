# Project Setup

## Frontend - React

1. Create docker container and install react via `Vite`:

```shell
docker run --rm -it -v $(pwd):/code -w /code node:22.12.0 sh -c "npm create vite@latest frontend -- --template react && cd frontend/ && npm install"
```

1. Create docker ignore file `.dockerignore`:

```text
README.md
frontend/node_modules/
```

3. Create docker file for frontend container `Dockerfile.frontend`:

```dockerfile
FROM node

COPY ./frontend /frontend
RUN rm -rf /frontend/node_modules

WORKDIR /frontend
RUN npm ci

CMD [ "npm", "run", "dev" ]
```

4. Create docker compose file `docker-compose.yaml`:

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

## Backend - Django

1. Create the requirement file `requirements.txt`:

```text
Django==5.1.4
```

### Docker File

Create `Dockerfile.backend` and use the following:

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

### Docker Compose

Add a new service to `docker-compose.yaml` file as follows:

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

### Test Container

Test to see whether the container and dockerfile runs without any error by using:

```shell
docker build .
```

### Setup Django on the Container

Install Django on the container directly by using:

```shell
docker compose run --rm backend sh -c "django-admin startproject backend ."
```

### Create Local Python Env

To get a better code experience, it is okay to install django locally in a isolated env by using the following:

```shell
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Add a Core APP to Django

To add a core app to Django run the following:

```shell
docker compose run --rm backend sh -c "python manage.py startapp core"
```

### Run DB Migration

To run a database migration in Django in container run the following:

```shell
docker compose run --rm backend sh -c "python manage.py makemigrations"
docker compose run --rm backend sh -c "python manage.py migrate"
```

### Create Admin

To create an admin user for Django accessing admin portal:

```shell
docker compose run --rm backend sh -c "python manage.py createsuperuser"
```

### Connect to DB

```shell
docker compose exec db psql -U user -d db
```
