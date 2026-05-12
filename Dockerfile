FROM python:2.7-slim

# Fix Debian Buster EOL repositories
RUN sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    sed -i 's|security.debian.org/debian-security|archive.debian.org/debian-security|g' /etc/apt/sources.list && \
    sed -i '/buster-updates/d' /etc/apt/sources.list && \
    echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid-until

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev \
    gettext \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN sed -i 's/from uuid import UUID, uuid4 as _uuid4, _uuid_generate_random/from uuid import UUID, uuid4 as _uuid4/' /usr/local/lib/python2.7/site-packages/kombu/utils/__init__.py
RUN sed -i "s/from filer.models import mixins/import importlib; mixins = importlib.import_module('filer.models.mixins')/" /usr/local/lib/python2.7/site-packages/filer/models/filemodels.py
RUN sed -i 's/from polymorphic import PolymorphicModel, PolymorphicManager/from polymorphic.models import PolymorphicModel\nfrom polymorphic.managers import PolymorphicManager/' /usr/local/lib/python2.7/site-packages/filer/models/filemodels.py

# Gunicorn is needed for production serving
RUN pip install --no-cache-dir gunicorn

# Copy project files
COPY . /app/

# Setup entrypoint
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["gunicorn", "sportomatics.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
