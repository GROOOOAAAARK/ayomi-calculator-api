# Python FastAPI Calculator

This is a simple Python FastAPI RPN Calculator implementation.

## Install and run the project

```bash
make install-project

source .envrc

make run
```

Or

```bash
pipenv install

source .envrc

python -m app
```
### E2E tests

Use the postman collection in `tests/e2e` to run the tests.
You just have to set the environment variable `api_url` to `localhost:8000`.

## Docker

Run the project with docker:

```bash
docker build --no-cache -f docker/app.Dockerfile -t ayomi-api .
docker network create --attachable ayomi-network
docker compose -f docker/docker-compose.yml up
```

