# User Service

User service is a simple CRUD Web API that adheres to the principles of Clean Architecture,
uses some DDD tactical patterns and follows CQRS

![List of endpoints](https://i.imgur.com/suyBIgX.png)

## Endpoints

#### GET /healthcheck
```bash
curl -X "GET" "http://localhost:5000/healthcheck"
```
```json
{"status": "ok"}
```

#### POST /users/

```bash
curl -X "POST" \
  "http://127.0.0.1:5000/users/" \
  -d '{
      "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "username": "username",
      "first_name": "string",
      "last_name": "string"
  }'
```
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "username": "username",
  "first_name": "string",
  "last_name": "string",
  "deleted": false
}
```

#### GET /users/
```bash
curl -X "GET" "http://127.0.0.1:5000/users/?offset=0&limit=1000&order=asc"
# Equivalent to http://127.0.0.1:5000/users/
```
```json
{
  "users": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66ffa6",
      "username": "username",
      "first_name": "string",
      "last_name": "string",
      "deleted": false
    },
    {
      "id": "3fa85f64-5717-4562-b3fc-2c9f3f66ffa1",
      "first_name": "string",
      "last_name": "string",
      "deleted": true
    }
  ]
}
```

## Dependencies

### Infrastructure

- [Postgres](https://www.postgresql.org/docs/current/index.html) — Database
- [RabbitMQ](https://www.rabbitmq.com/) — The queue used to publish events
- [Docker](https://docs.docker.com/) — For deployment

### Grafana stack

- [Grafana](https://grafana.com/docs/grafana/latest/) — Web view for logs
- [Loki](https://grafana.com/docs/loki/latest/) — A platform to store and query logs
- [Vector.dev](https://vector.dev) — A tool to collect logs and send them to Loki

###  Key python libs

- [FastAPI](https://fastapi.tiangolo.com/) — Async web framework
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/) — ORM for working with database
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) — Database schema migration tool
- [DI](https://www.adriangb.com/di/0.73.0/) — A dependency injection tool for easy initialization and delivery of dependencies
- [didiator](https://github.com/SamWarden/didiator) — Mediator to interact with application layer and publish events
- [adaptix](https://dataclass-factory.readthedocs.io/en/3.x-develop/) (dataclass_factory 3.0a0) — Library for simple model serialization and mapping
- [structlog](https://structlog.org/) — For better logging config
- [aio-pika](https://aio-pika.readthedocs.io/) — Client to interact with RabbitMQ

### TODO

- [ ] Implement outbox pattern
- [X] Add auto-tests
- [X] Configure CI
