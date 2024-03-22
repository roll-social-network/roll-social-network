FROM python:3.12.1-alpine AS build-requirements

WORKDIR /home/app

RUN pip install pipenv
COPY Pipfile* .
RUN pipenv requirements > requirements.txt

FROM python:3.12-alpine

WORKDIR /home/app
EXPOSE 8000
ENV DEBUG 0

COPY --from=build-requirements /home/app/requirements.txt .
RUN apk add --no-cache postgresql-libs && \
        apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
        pip install psycopg2-binary \
                    psycopg2 \
                    django-storages --no-cache-dir && \
        pip install -r requirements.txt --no-cache-dir && \
        apk --purge del .build-deps
COPY manage.py .
COPY rollsocialnetwork rollsocialnetwork

ENTRYPOINT [ "daphne" ]
CMD [ "-b", "0.0.0.0", "rollsocialnetwork.asgi:application" ]
