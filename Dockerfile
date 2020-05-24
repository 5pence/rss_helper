FROM python:3.8-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME /code
ENV WORKON_HOME /pipenvs
ENV PIPENV_VENV_IN_PROJECT 1

RUN apt-get -qq update \
    && apt-get install -y --no-install-recommends \
        git-core tmux vim locales less \
        binutils \
    && rm -rf /var/lib/apt/lists/* \
    && echo 'alias ll="ls -l"' >> ~/.bashrc \
    && echo 'alias la="ls -la"' >> ~/.bashrc \
    && locale-gen \
    && pip install --upgrade pip \
    && pip install pipenv

COPY . /code/
WORKDIR $APP_HOME
RUN pipenv run pip freeze
RUN pipenv install

RUN pipenv --venv
RUN pipenv run pip freeze
