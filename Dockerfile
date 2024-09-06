FROM postgres:15

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    postgresql-server-dev-15

RUN git clone https://github.com/pgvector/pgvector.git && \
    cd pgvector && \
    make && \
    make install

RUN apt-get remove -y build-essential git postgresql-server-dev-15 && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /pgvector

COPY init.sql /docker-entrypoint-initdb.d/