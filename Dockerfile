FROM pytorch/pytorch:2.12.1-cuda13.2-cudnn9-devel

RUN groupadd -g 110 render || true

RUN apt update
RUN apt install -y ruby-full build-essential zlib1g-dev

WORKDIR /workspace
EXPOSE 4000

# Non-root user matching the host (override via --build-arg UID/GID)
ARG UID=1000
ARG GID=1000
ARG UNAME=dev

RUN set -ex; \
  EXISTING=$(getent passwd ${UID} | cut -d: -f1 || true); \
  if [ -n "${EXISTING}" ] && [ "${EXISTING}" != "${UNAME}" ]; then \
    usermod -l ${UNAME} -d /home/${UNAME} -m ${EXISTING}; \
    groupmod -n ${UNAME} $(getent group ${GID} | cut -d: -f1) || true; \
  elif [ -z "${EXISTING}" ]; then \
    (getent group ${GID} >/dev/null || groupadd -g ${GID} ${UNAME}); \
    useradd -m -u ${UID} -g ${GID} -s /bin/bash ${UNAME}; \
  fi; \
  groupadd -g 44 video 2>/dev/null || true; \
  usermod -aG render,video ${UNAME}

ENV HOME=/home/${UNAME}
ENV GEM_HOME=${HOME}/gems
ENV PATH=${GEM_HOME}/bin:${PATH}

USER ${UNAME}
CMD ["bash"]
