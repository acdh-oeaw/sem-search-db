FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

RUN apt-get update -y && apt-get install -y --no-install-recommends nginx vim curl \
    postgresql-common libpq-dev build-essential gcc g++ make pkg-config cmake ninja-build \
    skopeo \
    && rm -rf /var/lib/apt/lists/*
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

COPY nginx.default /etc/nginx/sites-available/default

WORKDIR /opt/app

# Install dependencies from lockfiles first so this layer is reused when only app code changes.
COPY pyproject.toml uv.lock /opt/app/
RUN uv sync --no-install-project --no-dev --frozen

# Download the model in its own cacheable layer.
COPY llama/download-model.sh /opt/app/llama/download-model.sh
RUN /opt/app/llama/download-model.sh

# Copy the rest of the application source last.
COPY . /opt/app

# start server
EXPOSE 80
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]