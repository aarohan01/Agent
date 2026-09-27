FROM quay.io/centos/centos:stream9

RUN dnf install -y python3.11 curl-minimal \
    && dnf clean all

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:/opt/venv/bin:$PATH"
ENV UV_PROJECT_ENVIRONMENT="/opt/venv"

WORKDIR /app

COPY . .

RUN uv sync --frozen

EXPOSE 8000

CMD fastapi run main.py --host 0.0.0.0 --port ${PORT:-8000}
