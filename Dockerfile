FROM python:3.12.1-alpine AS build-requirements

WORKDIR /home/app

RUN pip install pipenv
COPY Pipfile* .
RUN pipenv requirements > requirements.txt

FROM node:20.11-alpine AS build-ui

WORKDIR /home/app

COPY ui/package*.json .
RUN npm install
COPY ui .
RUN npm run build

FROM python:3.12-alpine as app

WORKDIR /home/app
EXPOSE 8000
ENV DEBUG 0
ENV STATIC_ROOT /home/app/statics/
ENV GEOIP_PATH /home/app/.geoip/

COPY --from=build-requirements /home/app/requirements.txt .
RUN apk add --no-cache postgresql-libs && \
        apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
        pip install psycopg2-binary \
                    psycopg2 \
                    django-storages \
                    channels-redis --no-cache-dir && \
        pip install -r requirements.txt --no-cache-dir && \
        apk --purge del .build-deps
COPY --from=build-ui /home/app/dist ui/dist
COPY manage.py .
COPY rollsocialnetwork rollsocialnetwork
RUN mkdir .geoip
COPY .geoip/download-database.sh .geoip/download-database.sh
RUN cd .geoip && ./download-database.sh
RUN python manage.py collectstatic --noinput

ENTRYPOINT [ "daphne" ]
CMD [ "-b", "0.0.0.0", "rollsocialnetwork.asgi:application" ]

FROM nginx:latest as statics

COPY --from=app /home/app/statics /usr/share/nginx/html
COPY nginx.statics.default.conf /etc/nginx/conf.d/default.conf
