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

## Run tests

### E2E tests

Use the postman collection in `tests/e2e` to run the tests.
You just have to set the environment variable `api_url` to `localhost:8000`.

## Docker

Run the project with docker:

```bash
docker build --no-cache -f docker/app.Dockerfile -t rpn-api .
docker network create --attachable rpn-network
docker compose -f docker/docker-compose.yml up
```

## Upgrades

- [ ] Handle multiple expressions in the same query
- [ ] Add more supported operations in expression evaluation
- [ ] Better read function in mongodb implementation
- [ ] Add more tests (adapters, use cases, e2e w k6)
  - [ ] Add tests on responses inside Postman collection
