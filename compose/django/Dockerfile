FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

#COPY ./compose/django/celery/worker/start /start-celeryworker
#RUN sed -i 's/\r$//g' /start-celeryworker
#RUN chmod +x /start-celeryworker
#
#COPY ./compose/django/celery/beat/start /start-celerybeat
#RUN sed -i 's/\r$//g' /start-celerybeat
#RUN chmod +x /start-celerybeat
#
#COPY ./compose/django/celery/flower/start /start-flower
#RUN sed -i 's/\r$//g' /start-flower
#RUN chmod +x /start-flower

WORKDIR /app
COPY . /app
RUN --mount=type=cache,id=custom-pip,target=/core/.cache/pip pip install -r /app/requirements.txt && pip install gunicorn

COPY ./compose/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

ENTRYPOINT ["/entrypoint"]