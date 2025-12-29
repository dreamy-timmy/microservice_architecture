# FROM python:3.10-slim

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# WORKDIR /app

# # Install system dependencies required to build some python packages
# RUN apt-get update \
# 	&& apt-get install -y --no-install-recommends \
# 	   build-essential \
# 	   gcc \
# 	   libpq-dev \
# 	&& rm -rf /var/lib/apt/lists/*

# # Install Python dependencies
# COPY requirements.txt /app/requirements.txt
# RUN pip install --no-cache-dir -r /app/requirements.txt

# # Copy application code
# COPY . /app

# # Create non-root user and switch
# RUN adduser --disabled-password --gecos "" appuser || true
# RUN chown -R appuser:appuser /app
# USER appuser

# EXPOSE 3000

# # Default command: run uvicorn
# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3000"]

FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3000"]
