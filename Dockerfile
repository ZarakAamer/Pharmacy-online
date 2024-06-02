FROM python:latest
LABEL maintainer="zarak.xyz"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /requirements.txt
COPY ./app /app
COPY ./scripts /scripts
COPY ./app/static/* /vol/web/static/
COPY ./app/media/* /vol/web/media/

EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt && \
    adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

WORKDIR /app

USER app

CMD ["run.sh"]
