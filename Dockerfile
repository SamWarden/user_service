FROM python:3.13-slim-bookworm AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    APP_PATH="/app" \
    UV_VERSION="0.6.14"

ENV VIRTUAL_ENV="$APP_PATH/.venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

FROM python-base AS builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc git \
    && rm -rf /var/lib/apt/lists/

WORKDIR $APP_PATH

RUN pip install --no-cache-dir "uv==$UV_VERSION"

COPY ./pyproject.toml ./uv.lock ./
RUN uv venv -p 3.13 \
    && uv sync --all-extras --no-install-project
COPY ./src ./src
RUN uv sync --all-extras --no-editable

FROM python-base AS runner

COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV

CMD ["python", "-Om", "user_service"]
