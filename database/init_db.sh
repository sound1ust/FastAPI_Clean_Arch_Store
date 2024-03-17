#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  create table if not exists products
(
    product_id integer generated by default as identity
        primary key,
    name       varchar(50) not null
        constraint constraint_name
            unique,
    category   varchar(50) not null,
    price      real        not null
);
EOSQL