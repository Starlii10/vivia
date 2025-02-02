# syntax=docker/dockerfile:1
# Python image
ARG PYTHON_VERSION=3.10.6
FROM python:${PYTHON_VERSION}-slim as base

# Python config
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /vivia

ARG UID=10001
RUN adduser \
--disabled-password \
--gecos "" \
--home "/nonexistent" \
--shell "/sbin/nologin" \
--no-create-home \
--uid "${UID}" \
appuser

# Get dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
--mount=type=bind,source=requirements.txt,target=requirements.txt \
python -m pip install -r requirements.txt

# Install llama-cpp-python
# default to CPU if CUDA is not enabled
ARG USE_CUDA=0
RUN if [ "$USE_CUDA" = "1" ]; then \
    apt-get update && apt-get install -y --no-install-recommends cuda-command-line-tools-11-4 cuda-libraries-dev-11-4; \
    CMAKE_ARGS="-DGGML_CUDA=on"; \
    else \
    CMAKE_ARGS="-DGGML_BLAS=on -DGGML_BLAS_VENDOR=OpenBLAS"; \
    fi

# Give appuser read/write access to /vivia
USER root
RUN chown -R appuser:appuser /vivia

USER appuser
COPY . .
EXPOSE 8000
# Expose pip ports for it to download dependencies (added by Starlii manually, Docker why are you like this)
EXPOSE 3128
EXPOSE 443

CMD ["python", "bot.py"]