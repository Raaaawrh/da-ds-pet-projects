FROM ubuntu:jammy

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~ Info about container and variables ~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
LABEL Author="anatolii.farenik@yandex.com"
ARG PROJECT_NAME=volleyball-matches-scraper

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~ Init build variables and env variables ~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
ARG GROUP_NAME=vscode \
    GROUP_ID=1000 \
    USER_NAME=vscode \
    USER_ID=1000 
    
ENV VIRTUAL_ENV=/home/${USER_NAME}/projects/${PROJECT_NAME}/.venv \
    PATH="$VIRTUAL_ENV/bin:$PATH" \
    PYTHONPATH=/home/${USER_NAME}/projects/${PROJECT_NAME} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \ 
    #
    TOR_SOCKS_PORT=9050 \
    TOR_CONTROL_PORT=9051 \
    TOR_PASSWORD=password


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~ Update system and install packages ~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # Timezone info
RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone \
    && \
    apt-get -y update \
    && \
    apt-get -y install \
    git \
    curl \
    tor \
    python3 \
    python3-pip \
    python3-venv \ 
    # Next are playwright's dependencies
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxkbcommon0 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    # And more playwright dependencies (don't know why despite using headless mode)
    libx11-xcb1 \
    libxcursor1 \
    libgtk-3-0 \
    libpangocairo-1.0-0 \
    libcairo-gobject2 \
    libgdk-pixbuf-2.0-0 \
    libcairo-gobject2 \
    libgdk-pixbuf-2.0-0 \
    && \
    rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~ Add non-root user and create catalogues ~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

RUN groupadd --gid ${GROUP_ID} ${GROUP_NAME} \
    && \
    useradd --home-dir /home/${USER_NAME} --create-home \
            --gid ${GROUP_ID}             --uid ${USER_ID} \
            --shell /bin/bash             --skel /dev/null ${USER_NAME} \
    && \
    mkdir -p /home/${USER_NAME}/projects/${PROJECT_NAME} \
    && \
    chown -R ${USER_NAME}:${GROUP_NAME} /home/${USER_NAME}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~ Copy files ~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
COPY torrc /etc/tor/torrc
USER ${USER_NAME}
WORKDIR /home/${USER_NAME}/projects/${PROJECT_NAME}
COPY requirements.txt .
# COPY utils ./utils/
# COPY volleyball-matches-scraper ./volleyball-matches-scraper/
# COPY --chown=${USER_NAME}:${GROUP_NAME} . /home/${USER_NAME}/projects/${PROJECT_NAME}/

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~ Create python env and install packages into it ~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
RUN python3 -m venv --system-site-packages .venv \
    && \
    . .venv/bin/activate \
    && \
    python3 -m pip install --no-cache-dir -r requirements.txt \
    && \ 
    python3 -m playwright install firefox

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~ Configure tor ~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
USER root
RUN echo "CookieAuthentication 0" >> /etc/tor/torrc && \
    echo "ControlPort ${TOR_CONTROL_PORT}" >> /etc/tor/torrc && \
    echo "SOCKSPort ${TOR_SOCKS_PORT}" >> /etc/tor/torrc && \
    echo "HashedControlPassword $(tor --hash-password ${TOR_PASSWORD} | tail -n 1)" >> /etc/tor/torrc

# Change user finally
# USER ${USER_NAME}