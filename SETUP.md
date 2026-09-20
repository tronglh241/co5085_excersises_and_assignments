# Setup

## 1. Overview

This is the setup guide for **Deep Learning and Its Applications in Computer Vision Course**. The project can be set up either via pip (manual, local environment) or via Docker (GPU or CPU containerized environment).

## 2. Environment

### 2.1. pip

#### 2.1.1. Prerequisites

TBD

#### 2.1.2. ...

TBD — manual/pip setup instructions will be added here.

### 2.2. Docker

The project ships with GPU and CPU Docker services defined in `compose.yml`.

#### 2.2.1. Prerequisites

- [Docker](https://docs.docker.com/get-docker/) with Docker Compose
- For the `gpu` service: an NVIDIA GPU with the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) installed on the host

#### 2.2.2. Build and start a container

For GPU (requires a host with NVIDIA GPU support configured for Docker):

```bash
docker compose up -d gpu
```

For CPU only:

```bash
docker compose up -d cpu
```

This builds the image (see `Dockerfile`) and starts the container in the background. The current directory is mounted into the container at `/workspace`, and the container runs as a non-root user matching your host UID/GID.

#### 2.2.3. Open a shell in the container

```bash
docker compose exec gpu bash
```

(use `cpu` instead of `gpu` if you started the CPU service)

#### 2.2.4. Ports

| Service | Host port | Container port |
|---|---|---|
| gpu | 4000 | 4000 |
| cpu | 4001 | 4000 |

## 3. Building the docs (Optional)

The docs are built with Jekyll for GitHub Pages. Run the following from inside the container shell:

```bash
gem install bundler
cd docs
bundle install
```

> `gem install bundler` and `bundle install` only need to be run once (or again later if dependencies change).

Then, to build and serve the docs:

```bash
bundle exec jekyll build
bundle exec jekyll serve --host 0.0.0.0 --port 4000
```

Once running, the docs site is served on port 4000 inside the container — visit `http://localhost:4000` (GPU service) or `http://localhost:4001` (CPU service) on your host.
