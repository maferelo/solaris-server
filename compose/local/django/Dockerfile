# define an alias for the specific python version used in this file.
FROM python:3.11.5-slim-bullseye as python

# Python build stage
FROM python as python-build-stage

ARG BUILD_ENVIRONMENT=local

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev

WORKDIR /tmp

# Requirements are installed here to ensure they will be cached.
COPY ./requirements .

# Create Python Dependency and Sub-Dependency Wheels.
RUN --mount=type=cache,target=/root/.cache/pip \
  pip wheel --wheel-dir /usr/src/app/wheels  \
  -r ${BUILD_ENVIRONMENT}.txt

# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

# Allow piped commands to fail at any step and run, log command
SHELL ["/bin/bash", "-ceux", "-o", "pipefail"]


# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  sudo \
  git \
  bash-completion \
  nano \
  ssh \
  # Commits signing dependencies
  gnupg2 \
  # Heroku CLI dependencies
  curl \
  # psycopg2 dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Install Heroku CLI
RUN curl https://cli-assets.heroku.com/install.sh | sh

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

# Create devcontainer user and add it to sudoers
RUN groupadd --gid 1000 dev-user \
  && useradd --uid 1000 --gid dev-user --shell /bin/bash --create-home dev-user \
  && echo dev-user ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/dev-user \
  && chmod 0440 /etc/sudoers.d/dev-user

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

USER dev-user

# Bash theme
RUN bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)"

WORKDIR ${APP_HOME}

COPY .pre-commit-config.yaml .
# Install pre-commit hooks
# Buildkit cache mount is used to speed up the build process
# https://docs.docker.com/develop/develop-images/build_enhancements/#using-cache-mounts-to-persist-cache-data
# then environments are persisted in the default pre-commit cache dir
# for the dev container user
RUN --mount=type=cache,target=/home/dev-user/pre-commit,uid=1000 \
  git init . \
  && cp -r "/home/dev-user/pre-commit" "/home/dev-user/.cache" \
  && pre-commit install --install-hooks \
  && cp -r "/home/dev-user/.cache/pre-commit" "/home/dev-user" \
  && mv ".git/hooks" "/home/dev-user"

USER root

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint \
  && chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start \
  && chmod +x /start

USER dev-user

# copy application code to WORKDIR
COPY . ${APP_HOME}

RUN \
  mkdir -p \
  /home/dev-user/.vscode-server/extensions

ENTRYPOINT ["/entrypoint"]
