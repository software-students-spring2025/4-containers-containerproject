# FROM python:3.11-slim

# WORKDIR /app

# COPY requirements.txt requirements.txt
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# COPY . .

# EXPOSE 3000

# CMD ["flask", "run", "--host=0.0.0.0"]

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_RUN_PORT=5001 \
    FLASK_RUN_HOST=0.0.0.0

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["flask", "run"]
