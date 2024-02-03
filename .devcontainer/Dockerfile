FROM python:3.12.1-bullseye

ENV NODE_MAJOR 20

RUN pip install pipenv
RUN apt update \
        && apt install -y ca-certificates curl gnupg \
        && mkdir -p /etc/apt/keyrings \
        && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
        && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
        && apt update \
        && apt install nodejs -y \
        && npm install -g npm@10.2.5
