# Project Setup

## React (Frontend) Setup

### React Docker

Create docker container and install react on it

```shell
docker run --rm -it -v $(pwd):/code -w /code node:22.12.0 sh -c "npm create vite@latest frontend -- --template react && cd frontend/ && npm install"
```

### Docker Ignore

Create `.dockerignore` and use the following:

```
README.md
frontend/node_modules/
```

### Docker File

Create `Dockerfile.frontend` and use the following:

```
FROM node

COPY ./frontend /frontend
RUN rm -rf /frontend/node_modules

WORKDIR /frontend
RUN npm ci

CMD [ "npm", "run", "dev" ]
```

### Docker Compose

Create `docker-compose.yaml` and use the following:

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

### Modify Vite Config

Edit the file `vite.config.js` and add the following line:

```js
export default defineConfig({
	plugins: [react()],
	server: { host: "0.0.0.0" },
});
```

### Start Container

```shell
docker compose up --watch --build
```

### Sync Docker to Local

The `watch` is one way sync from local to container, but if we for example install a package on the cointaner and want to sync it back to our local we can use the following:

```shell
docker compose run --rm -v $(pwd)/frontend:/frontend frontend sh -c "npm install axios"
```

### Restart Server

After installing a new package, we need to stop (control+c) and start the server again with:

```shell
docker compose up --watch --build
```

## Django (Backend) Setup

### Django Requirement File

First we create a file called requirements.txt and add the following to it:

```
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
