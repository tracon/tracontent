FROM python:3.9
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN groupadd -r tracontent && useradd -r -g tracontent tracontent && \
    pip install --no-cache-dir -U pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app
RUN env DEBUG=1 python manage.py collectstatic --noinput && \
    python -m compileall -q . && \
    mkdir -p /usr/src/app/media && \
    chown tracontent:tracontent /usr/src/app/media
VOLUME /usr/src/app/media
USER tracontent
EXPOSE 8000
ENTRYPOINT ["/usr/src/app/scripts/docker-entrypoint.sh"]
CMD ["gunicorn", "--bind=0.0.0.0", "--workers=4", "--access-logfile=-", "--capture-output", "tracontent.wsgi"]