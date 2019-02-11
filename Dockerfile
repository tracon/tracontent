FROM python:3.7
WORKDIR /usr/src/app
COPY requirements.txt requirements-production.txt /usr/src/app/
RUN groupadd -r tracontent && useradd -r -g tracontent tracontent && \
    pip install --no-cache-dir -r requirements.txt -r requirements-production.txt
COPY . /usr/src/app
RUN env DEBUG=1 python manage.py collectstatic --noinput && \
    python -m compileall -q . && \
    mkdir -p /usr/src/app/media && \
    chown tracontent:tracontent /usr/src/app/media
VOLUME /usr/src/app/media
USER tracontent
EXPOSE 8000
ENTRYPOINT ["/usr/src/app/scripts/docker-entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
