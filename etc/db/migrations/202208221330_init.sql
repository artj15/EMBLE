--migrate:up


CREATE TABLE horses
(
    id BIGSERIAL,
    horse_id INTEGER,
    horse_name VARCHAR,
    camera_id INTEGER,
    even_type VARCHAR,
    duration INTEGER,
    date TIMESTAMP,
    start INTEGER,
    stop INTEGER,
    absolute_start TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() at time zone 'utc'),
    absolute_stop TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL
);


--migrate:down


DROP TABLE horses;
