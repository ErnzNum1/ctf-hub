FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    CTF_DATA_DIR=/data

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# run as a normal user (uid 1000), not root
RUN useradd -m -u 1000 ctf && mkdir -p /data /app/static/videos /app/challenge_files \
    && chown -R ctf:ctf /data /app
USER ctf

EXPOSE 8000

# 1 worker + threads: the login throttle and the database setup assume one process
CMD ["gunicorn", "-w", "1", "--threads", "4", "--timeout", "600", "-b", "0.0.0.0:8000", "app:app"]
