FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential ffmpeg libsndfile1 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /app
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=live_social.settings
CMD ["gunicorn", "live_social.wsgi:application", "-w", "2", "-b", "0.0.0.0:8000"]
