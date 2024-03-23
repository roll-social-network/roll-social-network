# roll social network

**social networks in their essence.**

Crie redes sociais em sua essência. Participe de comunidades "rolls" para consumir e compartilhar fotos. Interaja com outros usuários curtindo suas postagens.

**roll social network** é um projeto de código livre sob a licença [MIT](LICENSE) desenvolvido com os frameworks [Django](https://www.djangoproject.com/) e [Vue](https://vuejs.org/).

*in English:*

Create social networks in their essence. Join communities "rolls" to consume and share photos. Interact with other users by liking their posts.

**roll social network** is an open source project under the [MIT](LICENSE) license developed with the [Django](https://www.djangoproject.com/) and [Vue](https://vuejs.org/) frameworks.

## Run

### Development mode

Requirements:

- Python 3.12
- [pipenv](https://pipenv.pypa.io/en/latest/)
- Node.js 20.11

Init frontend submodule:

```bash
$ git submodule init frontend
```

Install dependencies:

```bash
$ pipenv install --dev
$ cd frontend/ && npm install --include=dev
```

The default app settings are setted to run locally in development and watch mode.

Init database tables:

```bash
$ pipenv run dbmigrate
```

Run Django app web server in watch mode:

```bash
$ pipenv run dev
```

Build the Vue app and static style files running the frontend package in watch mode:

```bash
$ cd frontend/ && npm run watch
```

### Lint and Tests

Run [pylint](https://pylint.readthedocs.io/en/latest/):

```bash
$ pipenv run lint
```

Run [mypy](https://mypy-lang.org/) to check typing:

```bash
$ pipenv run check-typing
```

Run unit tests:

```bash
$ pipenv run tests
```

Run unit tests with code [coverage](https://coverage.readthedocs.io/):

```bash
$ pipenv run coverage
# print code coverage report
$ pipenv run coverage-report
```

### Local as Production

Using dockerization and the [Docker Compose definition](docker-compose.yml), you can up all containers and services required by roll social network as if it were in production mode.

```bash
$ docker compose up --build
```

Services diagram:

![Local as Production services diagram.](readme-imgs/roll-local-as-production.drawio.png)

## Settings and Environment Vars

This project follow The [Twelve-Factor App](https://12factor.net/) methodology so all settings can be defined through environment variables.
