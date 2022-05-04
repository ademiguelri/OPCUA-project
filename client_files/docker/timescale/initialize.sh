psql --username "$POSTGRES_USER" <<EOF
CREATE DATABASE thermostat WITH OWNER $POSTGRES_USER;
GRANT ALL PRIVILEGES ON DATABASE thermostat TO $POSTGRES_USER;

\c thermostat
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

CREATE TABLE therm1 (datetime TIMESTAMP, temp FLOAT, state VARCHAR (10), target INTEGER, power INTEGER);
SELECT create_hypertable('therm1', 'datetime');
EOF