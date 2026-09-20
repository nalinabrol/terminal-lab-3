FROM mcr.microsoft.com/devcontainers/cpp:1-ubuntu-24.04

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 nano less man-db coreutils diffutils grep \
    && rm -rf /var/lib/apt/lists/*
