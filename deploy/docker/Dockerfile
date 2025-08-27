FROM node:20-bookworm

# Install system dependencies: Python, Pip, Nginx, envsubst
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
     python3 python3-pip python3-venv nginx gettext-base \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy manifests for deterministic installs
COPY package.json package-lock.json ./
COPY apps/web/package.json apps/web/package.json
COPY requirements.txt /tmp/requirements.txt

# Create Python venv and install API deps early for better layer caching
RUN python3 -m venv /opt/venv \
  && . /opt/venv/bin/activate \
  && pip install --no-cache-dir --prefer-binary -r /tmp/requirements.txt

# Install web dependencies and build Next.js
RUN npm install --prefix apps/web
COPY apps/web apps/web
RUN npm run build --prefix apps/web

# Copy API source (deps already installed in venv)
COPY apps/api apps/api

# Nginx template and start script
COPY deploy/docker/nginx.conf.template /etc/nginx/templates/default.conf.template
COPY deploy/docker/start.sh /start.sh
RUN chmod +x /start.sh

# For local run convenience; Render will provide $PORT
EXPOSE 8080

ENV NODE_ENV=production \
    HOST=0.0.0.0 \
    NEXT_PORT=3000 \
    API_PORT=8000

# Ensure venv is on PATH
ENV PATH="/opt/venv/bin:${PATH}"

CMD ["/start.sh"]
