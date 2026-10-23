FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /srv/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
 && useradd --system --uid 10001 --create-home appuser
COPY --chown=appuser:appuser . .
USER 10001:10001
EXPOSE 8000
CMD ["gunicorn", "--workers=2", "--threads=4", "--bind=0.0.0.0:8000", "--access-logfile=-", "--error-logfile=-", "wsgi:app"]
